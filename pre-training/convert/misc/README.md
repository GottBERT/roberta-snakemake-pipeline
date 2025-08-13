# Model Checkpoint Conversion and Testing Utilities

This script demonstrates how to:
- Fix and adapt fairseq model checkpoints for compatibility with both fairseq and Hugging Face Transformers.
- Rename and update model parameters and configuration fields as needed.
- Test the fixed checkpoint with both fairseq and Hugging Face for masked language modeling.

## Usage

1. **Fix a fairseq checkpoint:**
   - Loads a checkpoint, updates config and BPE fields, renames parameters, and saves the fixed checkpoint.
2. **Test with fairseq:**
   - Loads the fixed checkpoint using `GottbertModel` and runs a fill-mask example.
3. **Test with Hugging Face Transformers:**
   - Loads the converted model and runs a fill-mask example.

See the script for details and adjust paths as needed for your environment.
