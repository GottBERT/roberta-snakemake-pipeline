
# SVM Data Files

This directory contains raw and processed files used for SVM-based filtering and data labeling.

## File Descriptions

- **test.raw**: Test set for RoBERTa training.
- **valid.raw**: Validation set for monitoring model perplexity during training.
- **label_studio.raw**: Version of `test.raw` without line breaks, formatted for import into Label Studio for manual annotation (spam vs. not spam).
- **label_studio-min.json**: Minimal JSON export from Label Studio containing text and labels.

## Creating `label_studio.raw`

To generate `label_studio.raw` from the Label Studio export:

```bash
jq -r '.[].text' files/SVM/label_studio-min.json > label_studio.raw
```

## Label Distribution

- **Total labeled samples:** 1800 (100%)
    - **Clean:** 1466 (81.5%)
    - **Other:** 334 (18.5%)
        - **Mixed:** 90
        - **Spam:** 244
