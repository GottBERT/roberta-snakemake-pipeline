# Tools


## Plot

This small tool is created to create a plot based on a fairseq log file, i.e. if you pipe the output of the optimizer into a file.
Beyond that, as we computed our models on TPUs, we created a shell command, which can be called periodically to sync the script from a gcloud VM.
If that's what you want to do, then you'll require the [gcloud sdk](https://cloud.google.com/sdk/docs/quickstart).

## Requirements

- python3
- `pip install -r plot/requirements.txt`
- [optional] [gcloud sdk](https://cloud.google.com/sdk/docs/quickstart)

## Example usage

