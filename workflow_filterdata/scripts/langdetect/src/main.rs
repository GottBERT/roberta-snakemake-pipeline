extern crate clap;
extern crate whatlang;

use std::fs::File;
use std::io::prelude::*;
use std::io::{self, BufRead};
use std::path::Path;

use clap::{App, Arg};
use whatlang::detect;

mod fix_encoding;

fn main() -> std::io::Result<()> {
    let matches = App::new("langdetect")
        .version("0.1.0")
        .author("Raphael Scheible <raphael.scheible@uniklinik-freiburg.de>")
        .about(
            "goes through a file and pipes line by line the content \n
                into fail and success given a language and a confidence threshold",
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
            Arg::with_name("filename_success")
                .short("s")
                .long("success")
                .takes_value(true)
                .required(true)
                .help("file with all succeeded lines"),
        )
        .arg(
            Arg::with_name("filename_fail")
                .short("f")
                .long("fail")
                .takes_value(true)
                .required(true)
                .help("file with all failed lines"),
        )
        .arg(
            Arg::with_name("filename_count")
                .short("c")
                .long("count")
                .takes_value(true)
                .required(true)
                .help("count of lines of replacements will be stored here"),
        )
        .arg(
            Arg::with_name("lang")
                .short("l")
                .long("lang")
                .takes_value(true)
                .help(
                    "Searched language (ex. German); Line must be this language to succeed.\n
                      https://docs.rs/whatlang/0.11.1/whatlang/enum.Lang.html",
                ),
        )
        .arg(
            Arg::with_name("threshold")
                .short("t")
                .long("threshold")
                .takes_value(true)
                .help("Confidence threshold which a sentence must reach to success."),
        )
        .get_matches();

    let filename_source = matches.value_of("filename_source").unwrap();
    let filename_success = matches.value_of("filename_success").unwrap();
    let filename_count = matches.value_of("filename_count").unwrap();
    let filename_fail = matches.value_of("filename_fail").unwrap();
    let lang = matches.value_of("lang").unwrap_or("German");
    let threshold: f64 = matches
        .value_of("threshold")
        .unwrap_or("0.8")
        .parse()
        .unwrap();

    let mut file_success = File::create(filename_success)?;
    let mut file_fail = File::create(filename_fail)?;
    let mut file_count = File::create(filename_count)?;

    // Encoding fix
    let chars = fix_encoding::symbols_map(lang);

    let mut replacements = 0;

    // File hosts must exist in current path before this produces output
    if let Ok(lines) = read_lines(filename_source) {
        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            if let Ok(mut document) = line {
                let mut fixed_doc = document.clone();

                for (c, fix) in chars.iter() {
                    fixed_doc = String::from(fixed_doc.replace(c, fix));
                }

                replacements += (fixed_doc != document) as i64;

                // detect language
                let detection = detect(&fixed_doc.to_string());

                // if language recognized
                if detection.is_some() {
                    // get information
                    let info = detection.unwrap();
                    let detected_lang = info.lang().eng_name();

                    // if right language and confidence high enough
                    if info.confidence() >= threshold && detected_lang == lang {
                        // write to success file
                        fixed_doc.push_str("\n");
                        file_success.write_all(fixed_doc.as_bytes())?;
                    }
                } else {
                    // write to fail file
                    document.push_str("\n");
                    file_fail.write_all(document.as_bytes())?;
                }
            }
        }
    }

    // write the count
    file_count.write_all( replacements.to_string().as_bytes() )?;
    
    // close files
    file_count.flush()?;
    file_success.flush()?;
    file_fail.flush()?;

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
