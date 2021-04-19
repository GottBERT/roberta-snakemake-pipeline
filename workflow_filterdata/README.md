# Filtering

## Example
In `files/example/de_dedup.txt` lies a file which is a small extract of the German OSCAR corpus. We can use it for a small test computation.
In order to run the entire pipeline just run the following lines **while located in the root folder of the project**:

```bash
snakemake -s workflow_filterdata/Snakefile --use-conda --config in_file=files/example/de_dedup.txt -j$(nproc --all)
```

For furhter insrucitons about the config parameters, which we pass in the example per command line, read `GIT_ROOT/config/preprocess.yaml`. It's also possible to define all parameters there.