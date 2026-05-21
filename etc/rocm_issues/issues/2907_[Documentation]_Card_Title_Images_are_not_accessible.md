# [Documentation]: Card Title Images are not accessible

> **Issue #2907**
> **状态**: closed
> **创建时间**: 2024-02-19T09:33:17Z
> **更新时间**: 2024-08-13T23:02:56Z
> **关闭时间**: 2024-08-13T23:02:56Z
> **作者**: Maetveis
> **标签**: Documentation
> **URL**: https://github.com/ROCm/ROCm/issues/2907

## 标签

- **Documentation** (颜色: #5319e7)

## 描述

### Description of errors

The titles for the "cards" are images with text. Alternative text is not provided. This is very bad for screen readers and search engines.

Ideally the text should be in HTML and only the background should be an image. This would also make the site more printer friendly. [Sphinx design allows custom css classes](https://sphinx-design.readthedocs.io/en/latest/css_classes.html) to be applied to elements that should make this fairly straightforward
At the very least description of these images need to be provided.

As an extra comment these images are quite large raster images, it would be nice to replace them with vector if possible graphics with smaller size.

### Attach any links, screenshots, or additional evidence you think will be helpful.

![image](https://github.com/ROCm/ROCm/assets/8176760/421121d1-894d-4553-b361-720f61527a46)
![image](https://github.com/ROCm/ROCm/assets/8176760/eb664ed1-c4d1-4695-8c35-9fe3b0ca5c6d)


---

## 评论 (3 条)

### 评论 #1 — samjwu (2024-02-20T16:32:10Z)

Additional reference: https://sphinx-design.readthedocs.io/en/latest/cards.html#card-images

Example

```
:img-background: images/particle_background.jpg
:class-card: sd-text-black
:img-alt: my text
```

---

### 评论 #2 — LisaDelaney (2024-02-20T17:17:27Z)

@Maetveis I've started this PR: https://github.com/ROCm/ROCm/pull/2910. Feel free to add your suggestions here...I was not able to get the text to overlay my image, which is why I opted for the existing approach. But if you're able to make that happen, I'm all for it.

---

### 评论 #3 — Maetveis (2024-02-21T08:41:43Z)

I think a good approach would be to have a custom CSS classes for these background banner images. Would you be able to share the source images without the text? If you don't want to upload publicly then you can also send it by e-mail. I could add them to rocm-docs-core.

I see that in #2910 you changed them to use jpg, what format are these originally?

---
