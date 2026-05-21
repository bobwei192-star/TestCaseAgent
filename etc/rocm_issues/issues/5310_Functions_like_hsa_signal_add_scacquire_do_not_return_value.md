# Functions like hsa_signal_add_scacquire do not return value

> **Issue #5310**
> **状态**: closed
> **创建时间**: 2025-09-12T16:08:35Z
> **更新时间**: 2025-11-03T15:19:39Z
> **关闭时间**: 2025-11-03T15:19:38Z
> **作者**: misos1
> **标签**: Under Investigation
> **URL**: https://github.com/ROCm/ROCm/issues/5310

## 标签

- **Under Investigation** (颜色: #0052cc)

## 负责人

- tcgu-amd

## 描述

What does this function actually "acquire"? ~It seems such functions which do not return anything with acquire semantics are unnecessary.~

``` c++
void HSA_API hsa_signal_add_scacquire(
    hsa_signal_t signal,
    hsa_signal_value_t value);
```

~If I need to "acquire" new value after such addition I cannot use `hsa_signal_load_relaxed`. I have to use `hsa_signal_load_scacquire` and then `hsa_signal_add_scacquire` is redundant and `hsa_signal_add_relaxed` would be enough (or `hsa_signal_add_screlease` in case of `hsa_signal_add_scacq_screl`).~


---

## 评论 (15 条)

### 评论 #1 — ppanchad-amd (2025-09-12T16:21:13Z)

Hi @misos1. Internal ticket has been created to assist with your question. Thanks!

---

### 评论 #2 — b-sumner (2025-09-12T17:01:28Z)

Hi @misos1. Familiarity with C++ std::memory_order orderings such as `memory_order_acquire` and `memory_order_seq_cst` may help.  Also https://hsafoundation.com/wp-content/uploads/2021/02/HSA-SysArch-1.2.pdf chapter 3 on the HSA memory consistency model may help.

---

### 评论 #3 — misos1 (2025-09-12T17:26:57Z)

~Yes I am actually pointing out that. How is `hsa_signal_add_scacquire` different from `hsa_signal_add_relaxed` if it does not return a value? Acquire-release semantics in C++ is talking about ordering between memory operations visible to the thread, specifically in case of atomic load between the value loaded during atomic operation and other loads. If atomic add does not return any value then there is no user visible read operation, so what sense has talking about ordering then?~

From HSA documentation: "scacq ordering is similar to seq_cst ordering for a load in C++11, not acquire ordering." - so `scacquire` is actually supposed to be different from C++ `acquire`. But looking at implementation `hsa_signal_add_scacquire` does something like this (on x64 with `X64_ORDER_WC=1`):

``` c++
__atomic_fetch_add(ptr, val, __ATOMIC_RELAXED);
_mm_lfence();
```

So still, if it does not return a value I am not sure what sense this fence has.


---

### 评论 #4 — tcgu-amd (2025-10-16T17:42:31Z)

Hi @misos1, sorry for the lack of follow ups. I think regardless if a value is being returned, it is still an RMW operation. scacquire ensures the sequential consistent ordering for the acquire operation globally (which is achieved through the __atomic_fetch_add operation). As far as I know, the fence is there to provide acquire ordering for subsequent operations. I am not sure how being user-readable or whether an value is returned matters in this case. 

---

### 评论 #5 — misos1 (2025-10-17T20:03:57Z)

### On acquire semantics

Here is great explanation about acquire and release semantics: https://preshing.com/20120913/acquire-and-release-semantics:

Lets take this function:

``` c++
int atomic_add(int *ptr, int val)
{
  int ret = __atomic_fetch_add(ptr, val, __ATOMIC_RELAXED);
  _mm_lfence();
  return ret;
}
```

Then in code like this the load of value `a` is ordered before the load of `b` (lets say a == 0 meant that the payload is ready to read so only after that we can read it) and any other subsequent loads or stores:

``` c++
int *signal;
int *payload;
...
int a = atomic_add(signal, -1);
if(a == 0)
{
  int b = *payload;
  ...
}
```

~Now if `atomic_add` did not return anything then there is no sense to talk about ordering of what `__atomic_fetch_add` loaded. That value was discarded and it does not have any effect, it is not observable. It is irrelevant whether it is loaded before or after subsequent loads or stores. So now the only effect `_mm_lfence` has is that `atomic_add` orders all loads that happened "above" it before all subsequent loads and stores. It acts as an atomic fence. But `hsa_signal_add_scacquire` is supposed to be an atomic operation, it would not be good to use it in place of an atomic fence. Atomic fences order all previous memory operations (of specific type) before all subsequent memory operations (of specific type). But atomic operation is expected to only order the value it operates on with previous/subsequent memory operations (although in x64 instruction set there is no distinction). So what use `hsa_signal_add_scacquire` (with regards to `hsa_signal_add_relaxed`) could have except as an unintentional atomic fence?~

And it does not need to return a value for it to have an "acquire effect". For example if `hsa_signal_wait_scacquire` did not return anything (and always waited until the condition is satisfied without spurious returns) then it would be an acquire operation because it only returns after the right value is loaded and subsequent memory operations are ordered after. This "waiting finished" is the needed effect for acquire semantics to make sense with this function.

~Acquire does not apply to operations that are RMW internally but do not "read" value and `hsa_signal_add_scacquire` as operation does not "read" anything in this context. It acts just as a store with some "magic" that the resulting stored value depends on the original value in that memory place.~

### On sequential consistency

`__atomic_fetch_add(ptr, val, __ATOMIC_RELAXED)` does not provide sequential consistency. Not even with `LoadLoad` and `LoadStore` barrier which `_mm_lfence` acts like. But incidentally on x64 `__atomic_fetch_add(ptr, val, __ATOMIC_RELAXED)` produces the same asm as `__atomic_fetch_add(ptr, val, __ATOMIC_SEQ_CST)` because atomic RMW operations act as full barriers (but here is also important to consider compiler vs cpu reordering). At least with regard to "normal" memory. It is unclear to me whether it is enough for WC or `mfence` is required (either in general or maybe just some intel processors require `mfence`?). But "ROCR-Runtime-amd-staging/runtime/hsa-runtime/core/util/atomic_helpers.h" suggests that `mfence` should be used for sequential consistency and then `hsa_signal_add_scacquire` may not be sequentially consistent even on x64 (with regard to WC).

Now what about other "hsa sc" operations which are not RMW so are not sequentially consistent with regard to "normal" memory by accident? There is an example that demonstrates that `hsa_signal_load_scacquire` and `hsa_signal_store_screlease` are in fact not sequentially consistent:

``` c++
#include <thread>
#include <hsa/hsa.h>
#include <xmmintrin.h>

int main()
{
	hsa_init();
	hsa_signal_t sig1, sig2;
	hsa_signal_create(0, 0, NULL, &sig1);
	hsa_signal_create(0, 0, NULL, &sig2);
	int both_zero = 0;
	int total = 0;
	while(true)
	{
		hsa_signal_store_screlease(sig1, 0);
		hsa_signal_store_screlease(sig2, 0);
		std::atomic_int r1, r2;
		std::thread t1([&]()
		{
			hsa_signal_store_screlease(sig1, 1);
			//_mm_mfence();
			r1 = hsa_signal_load_scacquire(sig2);
		});
		std::thread t2([&]()
		{
			hsa_signal_store_screlease(sig2, 1);
			//_mm_mfence();
			r2 = hsa_signal_load_scacquire(sig1);
		});
		t1.join();
		t2.join();
		if(r1 == 0 && r2 == 0)both_zero++;
		total++;
		if(total % 10000 == 0)printf("both zero times %i   total times %i\n", both_zero, total);
	}
}
```

Possible output:

```
...
both zero times 11   total times 3220000
...
```

There is nothing that prevents `StoreLoad` reordering. `hsa_signal_load_scacquire` is `__atomic_load(__ATOMIC_RELAXED)` followed by `lfence` and `hsa_signal_store_screlease` is `sfence` followed by `__atomic_store(__ATOMIC_RELAXED)`

### Suggestion

I do not think that these `hsa_signal_...` operations should be always sequentially consistent. Why to not make them in some more "standard" way like mentioned clang/gcc atomics `__atomic_...` or C11 or opencl standard atomics so they all would take parameter for ordering which would be one of `relaxed`, `acquire`, `release`, `acq_rel` or `seq_cst`? And all RMW would return the value. So for example instead of:

``` c++
void HSA_API hsa_signal_add_scacquire(
    hsa_signal_t signal,
    hsa_signal_value_t value);
```

There would be for example:

``` c++
hsa_signal_value_t HSA_API hsa_signal_fetch_add(
    hsa_signal_t signal,
    hsa_signal_value_t value,
    hsa_memory_order_t order);
```

Like are done "__ockl_..." counterparts like `__ockl_hsa_signal_add`:

``` c++
extern void OCKL_MANGLE_T(hsa_signal,add)(hsa_signal_t sig, long value, __ockl_memory_order mem_order);
```

Except that with "__ockl_..." versions there is also missing return value which is another suggestion to also fix them to return the value and rename them to `__ockl_hsa_signal_fetch_add` for example. (I am aware that "ockl" functions are probably meant to be internal but why not fix them also?)

Also I am not sure about what sense has to have wait operations like `hsa_signal_wait_scacquire` to be able to stop waiting spuriously as is mentioned in: https://hsafoundation.com/wp-content/uploads/2021/02/HSA-SysArch-1.2.pdf

"Signal wait operations may return sporadically. There is no guarantee that the signal
value satisfies the wait condition on return. The caller must confirm whether the signal
value has satisfied the wait condition"


---

### 评论 #6 — tcgu-amd (2025-10-17T21:31:31Z)

Hi @misos1, thanks a lot for the detailed and thorough explanation! I definitely understand where you coming from better now. However, I am still a bit confused. I am not sure if I understand "Acquire does not apply to operations that are RMW internally but do not "read" value." How can it have RMW (i.e. *read*-modify-write), without *reading* values?  Also,though I agree with returning a value would be ergonomic, but unless I am mistaken, the atomic_add modifies the signal value in place, so you should still be able to retrieve the value after the acquire?

~Regarding to sequential consistency, I don't think there's anything wrong with the example you provided. Afaik, SC only establishes a single global order of SC operations, but loads can appear in that global order before the stores they are reading “against.” As a result L2(sig1), L1(sig2), S1(sig1=1), S2(sig2=1) is just a valid ordering. SC only forbids inconsistencies where different threads observe conflicting orders of SC stores.~

Note: This is incorrect, as pointed out by @misos1. 

---

### 评论 #7 — misos1 (2025-10-18T21:55:48Z)

> However, I am still a bit confused. I am not sure if I understand "Acquire does not apply to operations that are RMW internally but do not "read" value." How can it have RMW (i.e. _read_-modify-write), without _reading_ values? Also,though I agree with returning a value would be ergonomic, but unless I am mistaken, the atomic_add modifies the signal value in place, so you should still be able to retrieve the value after the acquire?

~It does not read value in the sense that it is unobservable to the outside of the function.~

Not only ergonomic. Actually, what seems I overlooked in this issue description, it is impossible to consistently read the value on which atomic add actually operated if that value is read afterwards as another thread may have changed it between atomic add and following atomic read in current thread. Atomic add which does not return a value cannot do everything that atomic add which does return a value can do. Imagine for example if `hsa_queue_add_write_index` did not return a value. It would be impossible to use it in the process of AQL packet submissions into multiproducer queues.

But lets pretend that is not a problem. Imagine we have `hsa_signal_add` followed by `hsa_signal_load` and want acquire semantics. Lets go through 3 possible combinations:

1.

``` c++
hsa_signal_add_scacquire(signal, val);
result = hsa_signal_load_relaxed(signal);
if(result == 0)p = *payload; 
```

Which translates roughly to:

``` c++
__atomic_fetch_add(ptr, val, __ATOMIC_RELAXED);
_mm_lfence();
result = __atomic_load(ptr, __ATOMIC_RELAXED);
if(result == 0)p = *payload; 
```

~This does not establish acquire semantics because our actual read is not acquire, it needs a fence between reading result and payload (lets suppose that `_mm_lfence` is needed because payload is in memory from which loads can be reordered with other loads).~

2.

``` c++
hsa_signal_add_scacquire(signal, val);
result = hsa_signal_load_scacquire(signal);
if(result == 0)p = *payload; 
```

``` c++
__atomic_fetch_add(ptr, val, __ATOMIC_RELAXED);
_mm_lfence();
result = __atomic_load(ptr, __ATOMIC_RELAXED);
_mm_lfence();
if(result == 0)p = *payload; 
```

Ok but the fence between atomic add and atomic load is unnecessary here because load from the same variable cannot be reordered with previous store to it.

3.

``` c++
hsa_signal_add_relaxed(signal, val);
result = hsa_signal_load_scacquire(signal);
if(result == 0)p = *payload; 
```

``` c++
__atomic_fetch_add(ptr, val, __ATOMIC_RELAXED);
result = __atomic_load(ptr, __ATOMIC_RELAXED);
_mm_lfence();
if(result == 0)p = *payload; 
```

Ok. Now we did not use `hsa_signal_add_scacquire`. ~It does not have any use here.~


> Regarding to sequential consistency, I don't think there's anything wrong with the example you provided. Afaik, SC only establishes a single global order of SC operations, but loads can appear in that global order before the stores they are reading “against.” As a result L2(sig1), L1(sig2), S1(sig1=1), S2(sig2=1) is just a valid ordering. SC only forbids inconsistencies where different threads observe conflicting orders of SC stores.

This implies that sequential consistent stores cannot reorder with following sequential consistent loads. Sequential consistency includes all seq_cst operations, not only stores:

https://eel.is/c++draft/atomics.order#4

"There is a single total order S on **all memory_order​::​seq_cst operations**, including fences, that satisfies the following constraints[.](https://eel.is/c++draft/atomics.order#4.sentence-1) First, **if A and B are memory_order​::​seq_cst operations and A strongly happens before B, then A precedes B in S**[.](https://eel.is/c++draft/atomics.order#4.sentence-2) Second, for every pair of atomic operations A and B on an object M, where A is coherence-ordered before B, the following four conditions are required to be satisfied by S:"

"[Note [2](https://eel.is/c++draft/atomics.order#note-2): This definition ensures that S is consistent with the modification order of any atomic object M[.](https://eel.is/c++draft/atomics.order#5.sentence-1) **It also ensures that a memory_order​::​seq_cst load A of M gets its value either from the last modification of M that precedes A in S** or from some non-memory_order​::​seq_cst modification of M that does not happen before any modification of M that precedes A in S[.](https://eel.is/c++draft/atomics.order#5.sentence-2) — end note]"

With operations S1(sig1=1), L1(sig2) in one thread and S2(sig2=1), L2(sig1) in another there are only these 6 possible total global orders:

S1(sig1=1), L1(sig2), S2(sig2=1), L2(sig1)
S1(sig1=1), S2(sig2=1), L1(sig2), L2(sig1)
S1(sig1=1), S2(sig2=1), L2(sig1), L1(sig2)
S2(sig2=1), S1(sig1=1), L1(sig2), L2(sig1)
S2(sig2=1), S1(sig1=1), L2(sig1), L1(sig2)
S2(sig2=1), L2(sig1), S1(sig1=1), L1(sig2)

Order L2(sig1), L1(sig2), S1(sig1=1), S2(sig2=1) is not valid.

https://stackoverflow.com/questions/70204442/does-c11-sequential-consistency-memory-order-forbid-store-buffer-litmus-test


---

### 评论 #8 — tcgu-amd (2025-10-20T21:32:34Z)

> Not only ergonomic. Actually, what seems I overlooked in this issue description, it is impossible to consistently read the value on which atomic add actually operated if that value is read afterwards as another thread may have changed it between atomic add and following atomic read in current thread.

This is true. However, I am not sure if providing such thread-safety guarantee is necessarily within the scope of the release-acquire semantics. Even the combined purpose of release-acquire semantics only provide a happens-before edge, and individually, their definition is even simpler. In the link you posted [here](https://preshing.com/20120913/acquire-and-release-semantics/) (good read, thanks for linking it btw), the acquire-release semantics are described simply as 
"
*Acquire semantics is a property that can only apply to operations that read from shared memory, whether they are [read-modify-write](http://preshing.com/20120612/an-introduction-to-lock-free-programming#atomic-rmw) operations or plain loads. The operation is then considered a read-acquire. **Acquire semantics prevent memory reordering of the read-acquire with any read or write operation that follows it in program order.***

*Release semantics is a property that can only apply to operations that write to shared memory, whether they are read-modify-write operations or plain stores. The operation is then considered a write-release. **Release semantics prevent memory reordering of the write-release with any read or write operation that precedes it in program order.***
"
Following this definition, which seems fair, what is being loaded/stored and whether they are user-visible should not matter, and the existing hsa acquire/release semantics seem to satisfy the description. Technically, as long as subsequent load operations happens after the RWM in `hsa_signal_add_sacquire`, the requirement of acquire semantics should be satisfied. If another thread changing the value of the signal is a concern, then using a stronger synchronization semantics such as a mutex may be desired. 

Hence, in the 3 scenarios you listed, both 1 and 2 should be perfectly valid, and 2 provides a stronger safety guarantee. 3 is not.

***

Regarding sequential consistency.

> Order L2(sig1), L1(sig2), S1(sig1=1), S2(sig2=1) is not valid.

Yes you are absolutely correct -- what I proposed was violation even of a relaxed definition of sequential consistency. Apologies, I did not know what I was talking about, and thanks for correcting me. 

That being said, after some digging and reviewing HSA's definition of sequential consistency, it seems that C++'s seq_cst is closer to the original [Lamport's sequential consistency](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1675439):

> R1:  Each processor issues memory requests in the order specified by its program.

> R2: Memory requests from all processors issued to an individual memory module are serviced from a single FIFO queue. Issuing a memory request consists of entering the request on this queue.

However, HSA's "seq_cst like" ordering does not strictly follow R2. Instead, it merely ensures speculators observe a consistent ordering. To illustrate, I modified example 3.13.1.1 to follow closer to your example

```
#include <thread>
#include <atomic>
#include <hsa/hsa.h>
#include <xmmintrin.h>

int main()
{
        hsa_init();
        hsa_signal_t sig1, sig2;
        hsa_signal_create(0, 0, NULL, &sig1);
        hsa_signal_create(0, 0, NULL, &sig2);
        int both_zero = 0;
        int sc_violation = 0;
        int total = 0;
        while(true)
        {
                hsa_signal_store_screlease(sig1, 0);
                hsa_signal_store_screlease(sig2, 0);
                std::atomic_int r1, r2, r3, r4;
                std::thread t1([&]()
                {
                        hsa_signal_store_screlease(sig1, 1);
                        //_mm_mfence();
                        r1 = hsa_signal_load_scacquire(sig2);
                        r3 = hsa_signal_load_scacquire(sig1);
                });
                std::thread t2([&]()
                {
                        hsa_signal_store_screlease(sig2, 1);
                        //_mm_mfence();
                        r2 = hsa_signal_load_scacquire(sig1);
                        r4 = hsa_signal_load_scacquire(sig2);
                });
                t1.join();
                t2.join();
                if(r1 == 0 && r2 == 0)both_zero++;
                total++;
                if(r1==1 && r1==r2 && r3==0 && r3==r4)sc_violation++;
                if(total % 10000 == 0)printf("both zero times %i   total times %i  sc violations %i\n", both_zero, total, sc_violation);
        }
}
```

And the result is

<img width="699" height="22" alt="Image" src="https://github.com/user-attachments/assets/6c8493aa-e5ad-4382-81f9-432965e8baa1" />

The example above should only be an extension to your original one. In this case, even S1(sig1), S2(sig2), L1(sig2), L2(sig1), L3(sig1), L4(sig2) may result in r1 == 0 and r2 == 0 simply because by time time L1 and L2 are reached, the result of S1 and S2 may not be visible yet. What hsa's sequential consistency prevents, as pointed out by 3.13.1.1, appears to be r1==1, r2==1, r3==0, r4==0, in which case the orders of change of sig1 and sig2 are conflicting. As you can see, this does not happen in this example. 

---

### 评论 #9 — misos1 (2025-10-21T16:28:46Z)

> Following this definition, which seems fair, what is being loaded/stored and whether they are user-visible should not matter, and the existing hsa acquire/release semantics seem to satisfy the description. Technically, as long as subsequent load operations happens after the RWM in `hsa_signal_add_sacquire`, the requirement of acquire semantics should be satisfied. If another thread changing the value of the signal is a concern, then using a stronger synchronization semantics such as a mutex may be desired.
> 
> Hence, in the 3 scenarios you listed, both 1 and 2 should be perfectly valid, and 2 provides a stronger safety guarantee. 3 is not.

I realized that my example is probably confusingly incomplete. I did not properly define the release part of synchronizes-with relationship.

Here is little modified example using C++ atomics (rather a pseudocode):

``` c++
atomic_int ready = 0;
int *payload;

void thread1()
{
	*payload = 42;
	atomic_store(ready, 1, release);
}

void thread2()
{
	if(atomic_fetch_add(ready, 0, acquire) == 1)
	{
		int p = *payload;
		printf("%i\n", p);
	}
}
```

Now using hsa signals:

``` c++
hsa_signal_t ready; // with signal value initialized to 0
int *payload;

void thread1()
{
	*payload = 42;
	hsa_signal_store_screlease(ready, 1);
}

void thread2()
{
	hsa_signal_add_relaxed(ready, 0);
	if(hsa_signal_load_scacquire(ready) == 1)
	{
		int p = *payload;
		printf("%i\n", p);
	}
}
```

I abused atomic add a little bit here and used is as atomic load so there is another a little more complex example (atomic reference counting):

``` c++
atomic_int sig = 2;
int *payload1, *payload2;

void thread1()
{
	*payload1 = 1;
	if(atomic_fetch_add(sig, -1, acquire_release) == 0)
	{
		int p = *payload2;
		printf("thread1: %i\n", p);
	}
}

void thread2()
{
	*payload2 = 2;
	if(atomic_fetch_add(sig, -1, acquire_release) == 0)
	{
		int p = *payload1;
		printf("thread2: %i\n", p);
	}
}
```

Using hsa signals:

``` c++
hsa_signal_t sig; // with signal value initialized to 2
int *payload1, *payload2;

void thread1()
{
	*payload1 = 1;
	hsa_signal_add_screlease(sig, -1);
	if(hsa_signal_load_scacquire(sig) == 0)
	{
		int p = *payload2;
		printf("thread1: %i\n", p);
	}
}

void thread2()
{
	*payload2 = 2;
	hsa_signal_add_screlease(sig, -1);
	if(hsa_signal_load_scacquire(sig) == 0)
	{
		int p = *payload1;
		printf("thread2: %i\n", p);
	}
}
```

Actual `load` here is what needs to be `acquire` so it will not be reordered with reading from `payload` (which can be done only when ref count is zero and all writing to it must be done before that). It is not enough for `signal_add` to be `acquire` in both these cases and so no need for acquire `atomic_add`. If both are `acquire` this does not provide any stronger guarantee. (And also this implementation would not work well for reference counting as it could enter IFs in both threads which is supposed to happen only once when reference count is zero.)

With these examples I am trying to show that `acquire-release` semantics is bound not only to signalling some flag but also actually observing that flag in another thread and based on that do plain reading and there is then established that `synchronizes-with` relationship where we can pass data with plain writes and reads. Purpose of `acquire-release` is to be able to use plain reads/writes elsewhere. And so operation which does not provide any observable effect does not need to be `acquire`, there is no purpose to do so.

---

> That being said, after some digging and reviewing HSA's definition of sequential consistency, it seems that C++'s seq_cst is closer to the original [Lamport's sequential consistency](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1675439):

Under 3.10 "Sequentially consistent synchronization order":

"In a candidate execution, there is a total apparent order of **all synchronization operations with release,
acquire**, or acquire-release semantics in a single scope instance. This order is called Sequentially Consistent
Synchronization Order"

This to me looks like C++ seq_cst. It includes in that total order also all `acquire` operations (so all RMW acquire and all load acquire).

In 3.13.3 "Non-sequentially consistent execution" there is example like I provided but using relaxed atomics.

"The following examples use relaxed atomics, are HSA-race-free, and can result in non-sequentially
consistent executions."

"In the above example, a valid outcome (though not the only valid outcome) at the end of execution is $s1 =
$s2 = 0. Note that in that execution, there is no total, globally visible order (i.e., sequentially consistent
order) of memory operations."

With C++ seq_cst all outcomes except $s1 = $s2 = 0 are allowed. If HSA seq_cst allows $s1 = $s2 = 0 then this wording looks contradictory because in that case that example would work the same without regard whether it is used relaxed or HSA seq_cst. And it would be pointless to have such an example here. It rather looks like HSA seq_cst also forbids `StoreLoad` reorder like C++ seq_cst, in that case my point about some hsa signal functions not being sequentially consistent would still hold. So in my example r1 = r2 = 0 should not happen as it uses HSA sequentially consistent order.

Again, maybe it is not a very good idea to have only `seq_cst` operations. Some have additional overhead on x64. I suppose that the HSA memory model was mainly intended for GPUs where sequential consistency seems to be equally cheap/expensive as acquire-release (at least on very few GPUs where I looked how these atomics are compiled into assembler).

---

### 评论 #10 — tcgu-amd (2025-10-21T17:41:45Z)

> Actual load here is what needs to be acquire so it will not be reordered with reading from payload (which can be done only when ref count is zero and all writing to it must be done before that). It is not enough for signal_add to be acquire in both these cases and so no need for acquire atomic_add. 

I am not sure that's correct. In your first example, you need the add to be acquire, otherwise load-relaxed can be ordered before the add. On the contrary, the load on the signal itself can be relaxed (as long as there's no external 3rd thread changing its value), because we have now made sure it always happens after the add. I can't really see how the signal load can be reordered with "reading from the payload", since the later is inside a branch. The conditional dependency should ensure that it only take place after the condition is met inside the if statement. 

I took a look at 3.13.3, and I think you have raised a good point. It is possible that at some point the implementation/interpretation of hsa's sc semantics diverged from the original. I will get back to you on that. @b-sumner if you can let us know your thoughts as well that would be much appreciated! 

---

### 评论 #11 — misos1 (2025-10-22T18:25:53Z)

> I am not sure that's correct. In your first example, you need the add to be acquire, otherwise load-relaxed can be ordered before the add.

That add stores to the same variable which is read by the following load. These cannot reorder in the "eyes" of the current thread. Every thread observes its own loads and stores as if in program order.

> On the contrary, the load on the signal itself can be relaxed (as long as there's no external 3rd thread changing its value), because we have now made sure it always happens after the add.

Note that even acquire or seq_cst does change much if there is an external 3rd thread changing that value (load can read "newer" value stored by that 3rd thread instead of what add stored).

> I can't really see how the signal load can be reordered with "reading from the payload", since the later is inside a branch. The conditional dependency should ensure that it only take place after the condition is met inside the if statement.

Signal value and payload (meaning `*payload` - variable where that pointer points, not the pointer itself) are different variables. Consume semantics does not apply here (about which there is another great article https://preshing.com/20140709/the-purpose-of-memory_order_consume-in-cpp11/). Imagine for example that the signal value is in a different cache line than `*payload` and the latter is not fresh enough when loading it in that if statement. Acquire should definitely be here.


---

### 评论 #12 — misos1 (2025-10-22T20:17:56Z)

> However, I am still a bit confused. I am not sure if I understand "Acquire does not apply to operations that are RMW internally but do not "read" value." How can it have RMW (i.e. _read_-modify-write), without _reading_ values?

I think I was finally able to find what I was searching for: https://eel.is/c++draft/atomics.order#2

"An atomic operation A that performs a release operation on an atomic object M synchronizes with an atomic operation B that performs an **acquire operation on M and takes its value from** any side effect in the release sequence headed by A[.](https://eel.is/c++draft/atomics.order#2.sentence-1)"

~Thus `hsa_signal_add_scacquire` is not an acquire operation. It cannot act as one and form synchronizes-with relationship with some other release operation.~

This is explained in detail in: https://preshing.com/20130823/the-synchronizes-with-relation/

Note that: "It all depends on whether the read-acquire sees the value written by the write-release, or not. That’s what the C++11 standard means when it says that atomic operation B must “take its value” from atomic operation A."

Also this may be interesting to read: https://preshing.com/20130702/the-happens-before-relation/

---

### 评论 #13 — tcgu-amd (2025-10-23T22:51:17Z)

> Note that: "It all depends on whether the read-acquire sees the value written by the write-release, or not. That’s what the C++11 standard means when it says that atomic operation B must “take its value” from atomic operation A."

In the context of the example you provided, I think that's true, in particular. In my previous reply, I overlooked the `hsa_signal_add_scacquire(ready, 0)` line. I agree that this line in fact does nothing meaningful and doesn't really provide a practical synchronization mechanism. 

However, the following modified version should work, right?
```
hsa_signal_t ready; // with signal value initialized to 0
int *payload;

void thread1()
{
	*payload = 42;
	hsa_signal_store_screlease(ready, 1);
}

void thread2()
{
	hsa_signal_add_scacquire(ready, 1);
	if(hsa_signal_load_relax(ready) == 2)
	{
		int p = *payload;
		printf("%i\n", p);
	}
}
```

Regarding my comment about conditional dependency, sorry I thought you were talking about the first example, my bad. 

In your second example's case, yes I do agree the load needs to be acquire. However, I don't think using this case to prove hsa_signal_add do not need an acquire variation is quite complete. `hsa_signal_add_sacquire` does produce a user visible effect, which is incrementing the signal by value, and it does fulfil the role of providing an acquire order. Saying the operation is not valid just because there are equivalent alternatives in certain cases isn't really fair. 




---

### 评论 #14 — misos1 (2025-10-27T16:15:50Z)

Yes, it seems that version is ok. It should work even if payload is loaded before `hsa_signal_load_relaxed`:

```c++
hsa_signal_add_scacquire(ready, 1);
int p = *payload;
// now if hsa_signal_load_relaxed(ready) == 2 then p must be 42
```

Because in this example `hsa_signal_load_relaxed` can return 2 only if `hsa_signal_add_scacquire` observed 1 (from release) and incremented it to 2. So I now see that `hsa_signal_add_scacquire` is actually not useless and can act as an acquire operation. However its use case seems rather obscure. It would be much better if it returned the value.


---

### 评论 #15 — tcgu-amd (2025-11-03T15:19:38Z)

Hi @misos1, I will be closing this issue for now since your original question has been answered. Regarding the SC issue, I was able to confirm that the behavior is intended, but it is different than seq_cst in C++. The SC only applies to synchronization operations within a scope instance, instead of a single order of operation across all atomics. Please feel free to follow up if you have any additional questions. 

---
