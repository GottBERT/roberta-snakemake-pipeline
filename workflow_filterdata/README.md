
# Data Filtering Workflow

This workflow provides a Snakemake pipeline for filtering and cleaning large-scale text corpora, such as the German OSCAR dataset. It includes steps for text cleaning, language detection, SVM-based filtering, and more.

## Example Usage
A small extract of the German OSCAR corpus is provided at `../files/example/de_dedup.txt`. You can use this file for a quick test run of the pipeline.

**To run the entire pipeline, execute the following command from the root folder of the project:**

```bash
snakemake --use-conda --config in_file=../files/example/de_dedup.txt -j$(nproc --all)
```

## Configuration
Pipeline parameters can be set via the command line as shown above, or by editing the configuration file at `workflow_filterdata/config.yaml`.

Refer to the config file for detailed descriptions of all available options.

## Output
The workflow will generate filtered and cleaned versions of your input data, along with intermediate files for each processing step. Output locations and formats are controlled by the configuration.


## Requirements
See the main project [README](../README.md) for requirements. All other dependencies are managed automatically via the provided Conda environments.

## Further Information
For more details on each step or troubleshooting, see the documentation in the respective scripts and config files.