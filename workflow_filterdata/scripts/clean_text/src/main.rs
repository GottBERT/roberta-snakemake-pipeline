// in order to work one needs to add python to LD_LIBRARY_PATH like:
// export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/anaconda3/lib/

use pyo3::prelude::*;
use pyo3::types::PyDict;
use std::fs::File;
use std::io::prelude::*;
use std::io::{self, BufRead};
use std::path::Path;

fn main() -> PyResult<()> {

    let filename_source = "/home/scheible/git/lrz/NLP/BERT/GottBERT/files/SVM/train_big_n.raw";
    let filename_target = "/home/scheible/git/lrz/NLP/BERT/GottBERT/files/SVM/train_big_n_clean.raw";

    Python::with_gil(|py| {
        let builtins = PyModule::import(py, "cleantext")?;
        let kwargs = PyDict::new(py);
        kwargs.set_item("lower", false)?;
        kwargs.set_item("fix_unicode", true)?;
        kwargs.set_item("no_emails", true)?;
        kwargs.set_item("no_phone_numbers", true)?;
        kwargs.set_item("no_emoji", true)?;
        kwargs.set_item("replace_with_url", "")?;
        kwargs.set_item("replace_with_email", "")?;
        kwargs.set_item("replace_with_phone_number", "")?;
        kwargs.set_item("lang", "de")?;

        let mut file_clean = File::create(filename_target)?;

        // File hosts must exist in current path before this produces output
        if let Ok(lines) = read_lines(filename_source) {
            // Consumes the iterator, returns an (Optional) String
            for line in lines {
                if let Ok(document) = line {
                    // let mut fixed_doc = document.clone();

                    let mut clean_line: String = builtins
                        .getattr("clean")?
                        .call((document,), Some(kwargs))?
                        .extract()?;
                    
                    clean_line.push_str("\n");
                    file_clean.write_all(clean_line.as_bytes())?;
                }
            }
        }
        file_clean.flush()?;

        Ok(())
    })
}

// The output is wrapped in a Result to allow matching on errors
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}