title: collections之Counter使用
date: 2016-10-02 10:20:55
tags:
    - Django
    - Python
    - Counter
categories:
---
在看Django源码时，知道了Counter，
```
# Check for duplicate app names.
counts = Counter(
    app_config.name for app_config in self.app_configs.values())
duplicates = [
    name for name, count in counts.most_common() if count > 1]
if duplicates:
    raise ImproperlyConfigured(
        "Application names aren't unique, "
        "duplicates: %s" % ", ".join(duplicates))
```
感觉很不错，比用dict统计方便多了，以后需要计数时，就用Counter。看来collections库是个宝库，要好好看看。
