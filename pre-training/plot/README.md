# Tools


## Plot

This small tool is created to create a plot based on a fairseq log file, i.e. if you pipe the output of the optimizer into a file.
Beyond that, as we computed our models on TPUs, we created a shell command, which can be called periodically to sync the script from a gcloud VM.
If that's what you want to do, then you'll require the [gcloud sdk](https://cloud.google.com/sdk/docs/quickstart).

## Requirements
- python3
- `pip install -r plot/requirements.txt`
- [optional] [gcloud sdk](https://cloud.google.com/sdk/docs/quickstart)

## Perplexity Plotting

`ppl_plot.py` can be used to visualize the perplexity curves from multiple fairseq log files. It parses log files, extracts perplexity values, and generates a combined plot for comparison.

### Example usage

Edit the `names` dictionary in `ppl_plot.py` to point to your log files, then run:

```bash
python ppl_plot.py
```

This will generate a file `perplexity-plot.png` with the perplexity curves for all specified models/logs.


### Plotting from a fairseq log file

```bash
python create_plot.py --logfile path/to/fairseq_train.log --output plot.pdf
```

### Syncing logs from a gcloud VM and plotting

```bash
# Sync logs from your TPU VM (requires gcloud SDK)
bash gcloud_sync_plot.sh
# Then plot as above
python create_plot.py --logfile synced_log.log --output plot.pdf
```

### Live plotting with remote log syncing

For live plotting with logs from a remote TPU VM, you need the `gcloud_sync_plot.sh` script (requires gcloud SDK):

```bash
watch -n 30 'bash gcloud_sync_plot.sh <TPU_VM_NAME> <LOG_FILE_ON_VM> [output_dir] [log_interval]'
```

The default for `log_interval` is 25 and output dir `./plot/`. This will periodically sync the log file from your TPU VM and update the PDF.
In case of a PDF viewer which updates automatically, you can live watch the plot evolving.


## Training Time Estimation

The script `compute_time_estimation.py` is designed for scenarios where model training is distributed across clusters, often resulting in multiple log files due to repeated or segmented training runs. To accurately estimate the total active training time, follow these steps:

1. **Unite Log Files:**
	- Collect all relevant log files generated during your training runs.
  - Copy the first log file and rename it e.g. `train.log`.
	- Append only the lines corresponding to active training steps of the other log files (typically lines containing `train_inner`) to the content of the very first log file. Also neglect the last lines that were executed after the last checkpoint save.

2. **Run the Script:**
	- Edit the `names` dictionary in `compute_time_estimation.py` to point to your unified log file(s).
	- Execute the script:

	  ```bash
	  python compute_time_estimation.py
	  ```

	- The script will parse the timestamps of training steps, ignore long gaps (e.g., queue or pause times), and report the total active training time and segments.

**Note:** The script uses a gap threshold (default: 300 minutes) to distinguish between active training and waiting/paused periods. Adjust this value as needed for your cluster environment.

This approach ensures that only the actual training time is measured, providing a more accurate estimate for distributed or interrupted training workflows.

