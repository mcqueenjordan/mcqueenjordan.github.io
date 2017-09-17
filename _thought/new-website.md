---
layout: thought
title: New Website Design
subtitle: Optimizing for Ease of Publishing
topics: ["website"]
name: new-website
published_date: 2017-06-24
category: post
---

The optimal process is the one that works. My previous website was dynamic,
loading its content from a database per-request. That was too heavyweight
for what I needed. As a result, I didn't publish to it much. It may have been
more impressively engineered than a simple static website, but it was
negatively impacting the latency of publishing.

In light of that, here is my new dead-simple static website, hosted using
files generated from markdown, stored in AWS' S3 and fronted with AWS
CloudFront.

