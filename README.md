# 📰 Cursory

Cursory is an open-source minimalistic news reader that lets you catch up with the most essential news from around the globe in 15+ languages. It is powered by Wikipedia.

> [!WARNING]
> Under active development. Expect bugs and breaking changes.

## ✨ Features

### 🔒 Privacy-first

No tracking, no ads, no cookies, no analytics, no third-party requests.

### 🚀 Lightning fast

Page size is usually under 100 KiB (including images!). This is accomplished by converting images to a modern format.

### 🌍 Supports 15+ languages

Supports many languages including English, Spanish, French, Russian, Korean, and more.

### ⏳ Stay up-to-date

Cursory is rebuilt every three hours with the latest news.

## Build

Make sure Python 3.8+ is installed.

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run build command

```bash
python build.py
```

After the build is complete, the `site` directory will contain the static website.
