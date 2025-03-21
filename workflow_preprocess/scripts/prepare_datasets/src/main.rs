extern crate clap;
extern crate linecount;
extern crate rand;

use std::fs::File;
use std::io::prelude::*;
use std::io::{self, BufRead};
use std::path::{Path, PathBuf};

use clap::{App, Arg};
use linecount::count_lines;
use rand::Rng;
use std::collections::HashSet;
use std::convert::TryInto;

fn main() -> std::io::Result<()> {
    let matches = App::new("prepare_datasets")
        .version("0.1.0")
        .author("Raphael Scheible <raphael.scheible@uniklinik-freiburg.de>")
        .about(
            "adds an empty line after each line in a document and \n
                splits the file in train/test/valid set",
        )
        .arg(
            Arg::with_name("filename_source")
                .short("i")
                .long("in")
                .required(true)
                .takes_value(true)
                .help("input file"),
        )
        .arg(
            Arg::with_name("dir_result")
                .short("o")
                .long("out")
                .takes_value(true)
                .required(true)
                .help("output folder for the results"),
        )
        .arg(
            Arg::with_name("n")
                .short("n")
                .long("num")
                .takes_value(true)
                .required(true)
                .help("number of lines of test and validation set"),
        )
        .get_matches();

    let n: usize = matches.value_of("n").unwrap().parse().unwrap();
    let filename_source = matches.value_of("filename_source").unwrap();
    let dir_result = matches.value_of("dir_result").unwrap();

    // paths to the files
    let path_train = PathBuf::from(dir_result).join("train.raw");
    let path_valid = PathBuf::from(dir_result).join("valid.raw");
    let path_test = PathBuf::from(dir_result).join("test.raw");

    // create files
    let mut file_train = File::create(path_train)?;
    let mut file_test = File::create(path_test)?;
    let mut file_valid = File::create(path_valid)?;

    println!("counting lines");

    // open file in order to count lines
    let file_source = File::open(filename_source)?;
    let count: u64 = count_lines(file_source).unwrap().try_into().unwrap();

    // random number generator
    let mut rng = rand::thread_rng();

    // create hash sets with line ids
    let mut idx_test: HashSet<u64> = HashSet::new();
    let mut idx_valid: HashSet<u64> = HashSet::new();

    println!("computing random sets");

    // create two distinct sets of random index values
    while idx_test.len() < n || idx_valid.len() < n {
        // random number generation
        let random_train: u64 = rng.gen_range(0, count).try_into().unwrap();

        if idx_test.len() < n
            && !idx_test.contains(&random_train)
            && !idx_valid.contains(&random_train)
        {
            idx_test.insert(random_train);
        }

        // random number generation
        let random_valid: u64 = rng.gen_range(0, count).try_into().unwrap();

        if idx_valid.len() < n
            && !idx_test.contains(&random_valid)
            && !idx_valid.contains(&random_valid)
        {
            idx_valid.insert(random_valid);
        }
    }

    println!("writing files");

    // File hosts must exist in current path before this produces output
    if let Ok(lines) = read_lines(filename_source) {
        let mut count = 0;

        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            if let Ok(mut document) = line {
                // add empty new line
                document.push_str("\n\n");

                // find out in which file to write the line
                if idx_test.contains(&count) {
                    // write to test
                    file_test.write_all(document.as_bytes())?;
                } else if idx_valid.contains(&count) {
                    // write to valid
                    file_valid.write_all(document.as_bytes())?;
                } else {
                    // write to train
                    file_train.write_all(document.as_bytes())?;
                }

                // increase line count by 1
                count = count + 1;
            }
        }
    }

    // close files
    file_train.flush()?;
    file_valid.flush()?;
    file_test.flush()?;

    Ok(())
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
