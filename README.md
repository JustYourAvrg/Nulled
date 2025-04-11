# Nulled Sol's RNG Macro

## Required items
- [Python](https://www.python.org) | 3.11 or higher
- [Bloxstrap](https://github.com/bloxstraplabs/bloxstrap) | Used for the aura and biome detection
- [tesseract-ocr](https://github.com/tesseract-ocr/tesseract/releases/tag/5.5.0) | Used for the auto merchant

> **Bloxstrap and tesseract-ocr aren't required** but needed for
> - **Auto Merchant** ( tesseract-ocr )
> - **Aura Detection/Clipping** ( bloxstrap )
> - **Biome Detection** ( bloxstrap )

If using **Aura Detection** or **Biome Detection**
please ensure in the bloxstrap setting you turn on
Enable activity tracking and show game activity

I also put the python installer, and the tesseract-ocr 5.5.0 installer in the `required_downloads` folder

---

## How to use

### Easy Setup
1. install the latest release in the releases page of the repo
2. download the .zip
3. extract the zip anywhere
4. run the exe file

---

### Manual Setup ( if you don't trust the .exe file )
```bash
cd "PATH_TO_NULLED"
python -m venv venv       # Optional but recommended
venv\Scripts\activate     # Optional
pip install -r requirements.txt
```

after setup, to run just type
```bash
python nulled.py
```


## Note
If something goes wrong and doesn't seem to work, check the errors_log.log file
