extern crate natural;

use polars::prelude::*;
use natural::tokenize::tokenize;


use std::{
    fs::File,
    io::{self, BufRead, BufReader},
    path::Path,
};

fn lines_from_file(filename: impl AsRef<Path>) -> Vec<String> {
    let file = File::open(filename).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .map(|l| l.expect("Could not parse line") as String)
        .collect()
}

fn main() {
    let filename_in = "/home/scheible/git/lrz/NLP/BERT/GottBERT/files/SVM/train_big_n.raw";

    // initialize vectors based on which the dataframe will finally be created
    let mut vec_stopword_ratio : Vec<f64> = Vec::new();
    let mut vec_punctuation_ratio : Vec<f64> = Vec::new();
    let mut vec_token_ratio : Vec<f64> = Vec::new();
    let mut vec_upper_ratio : Vec<f64> = Vec::new();
    let mut vec_upper_to_punct_ratio : Vec<f64> = Vec::new();
    let mut vec_num_tokens_original : Vec<u64> = Vec::new();
    let mut vec_num_unique_tokens_filtered : Vec<u64> = Vec::new();
    let mut vec_num_punctuation : Vec<u64> = Vec::new();
    let mut vec_num_upper : Vec<u64> = Vec::new();


    // read stopwords
    let stop_words = lines_from_file("/home/scheible/git/lrz/NLP/BERT/GottBERT/workflow_filterdata/scripts/compute_ratios/src/stopwords/german");

    // File hosts must exist in current path before this produces output
    if let Ok(lines) = read_lines(filename_in) {
        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            if let Ok(document) = line {
                // tokenize document
                let word_tokens : Vec<String> = tokenize(&document).into_iter().map(String::from).collect();

                // estimate non word tokens
                let mut token_string = document.clone();
                
                // remove word_tokens from token_string
                for token in &word_tokens {
                    token_string = token_string.replace(token, "");
                }

                let mut non_word_token : Vec<String> = token_string.replace(" ", "").chars().collect::<Vec<char>>()
                                                .into_iter().map(String::from).collect();

                // compute how many puncuations occur in document
                let num_punctuation = non_word_token.len() as u64;

                let mut tokens : Vec<String> = Vec::from(word_tokens.to_vec());
                tokens.append(&mut non_word_token);

                // number of tokens of the original document
                let num_tokens_original = tokens.len() as u64;

                // tokens without stopwords
                let mut filtered_tokens = Vec::new();
                for token in &word_tokens {
                    if !stop_words.iter().any(|i| i==token) {
                        filtered_tokens.push(token.to_string());
                    }
                }

                // compute stopword ratio, i.e. 1-|tokens without stop words|/|tokens of document|
                let mut stopword_ratio = 0.0;
                if word_tokens.len() > 0 {
                    stopword_ratio = 1.0 - filtered_tokens.len() as f64/num_tokens_original as f64;
                }

                // upper
                let mut upper_word_token : Vec<String> = Vec::new();
                for token in word_tokens {
                    if token.chars().collect::<Vec<char>>()[0].is_uppercase() {
                        upper_word_token.push(token);
                    }
                }

                // number of tokens which start with a upper case character
                let num_upper = upper_word_token.len() as u64;

                // number of unique tokens
                trait CountUnique {
                    fn unique_n(self) -> usize;
                }
                
                impl<I, T> CountUnique for I
                where
                    I: Iterator<Item = T>,
                    T: Eq + ::std::hash::Hash,
                {
                    fn unique_n(self) -> usize {
                        self.collect::<::std::collections::HashSet<_>>().len()
                    }
                }
                
                let num_unique_tokens_filtered = filtered_tokens.into_iter().unique_n() as u64;

                // compute puntuation ratio, i.e. |puncuation tokens|/|tokens of document|
                let mut punctuation_ratio = 0.0;
                if num_tokens_original > 0 {
                    punctuation_ratio = num_punctuation as f64/num_tokens_original as f64;
                }

                // compute token ratio, which describes the occurence of repeating words
                let mut token_ratio = 0.0;
                if num_tokens_original > 0 {
                    token_ratio = num_unique_tokens_filtered as f64/num_tokens_original as f64;
                }

                // ratio between upper word tokens and tokens in general, i.e. |upper case tokens|/|tokens of document|
                let mut upper_ratio = 0.0;
                if num_tokens_original > 0 {
                    upper_ratio = num_upper as f64/num_tokens_original as f64;
                }
                
                // after puctuation, in German, one continues to write in capital
                let mut upper_to_punct_ratio = 0.0;
                if num_punctuation > 0 && num_upper > 0 {
                upper_to_punct_ratio = (num_upper as f64/num_punctuation as f64) / num_upper as f64;
                }

                vec_stopword_ratio.push(stopword_ratio);
                vec_punctuation_ratio.push(punctuation_ratio);
                vec_token_ratio.push(token_ratio);
                vec_upper_ratio.push(upper_ratio);
                vec_upper_to_punct_ratio.push(upper_to_punct_ratio);
                vec_num_tokens_original.push(num_tokens_original);
                vec_num_unique_tokens_filtered.push(num_unique_tokens_filtered);
                vec_num_punctuation.push(num_punctuation);
                vec_num_upper.push(num_upper);

                // println!("stopword_ratio: {:?}", stopword_ratio);
                // println!("punctuation_ratio: {:?}", punctuation_ratio);
                // println!("#tokens_original: {:?}", num_tokens_original);
                // println!("#tokens_filtered: {:?}", num_unique_tokens_filtered);
                // println!("#tokens_puctuation: {:?}", num_punctuation);
                // println!("token_ratio: {:?}", token_ratio);
                // println!("#token_upper: {:?}", num_upper);
                // println!("upper_ratio: {:?}", upper_ratio);
                // println!("upper_to_punct_ratio: {:?}", upper_to_punct_ratio);
            }
        }
    }

    let s0 = ChunkedArray::<Float64Type>::from_vec("stopword_ratio", vec_stopword_ratio).into_series();
    let s1 = ChunkedArray::<Float64Type>::from_vec("punctuation_ratio", vec_punctuation_ratio).into_series();
    let s2 = ChunkedArray::<Float64Type>::from_vec("token_ratio", vec_token_ratio).into_series();
    let s3 = ChunkedArray::<Float64Type>::from_vec("upper_ratio", vec_upper_ratio).into_series();
    let s4 = ChunkedArray::<Float64Type>::from_vec("upper_to_punct_ratio", vec_upper_to_punct_ratio).into_series();
    let s5 = ChunkedArray::<UInt64Type>::from_vec("num_tokens_original", vec_num_tokens_original).into_series();
    let s6 = ChunkedArray::<UInt64Type>::from_vec("num_unique_tokens_filtered", vec_num_unique_tokens_filtered).into_series();
    let s7 = ChunkedArray::<UInt64Type>::from_vec("num_punctuation", vec_num_punctuation).into_series();
    let s8 = ChunkedArray::<UInt64Type>::from_vec("num_upper", vec_num_upper).into_series();
    
    let mut df_result = DataFrame::new(vec![s0, s1, s2, s3, s4, s5, s6, s7, s8]).unwrap();
    let mut file = std::fs::File::create("result.csv").unwrap();
    CsvWriter::new(&mut file).finish(&mut df_result).unwrap();

    // TODO: find a way to save to an exchange format to python and find a format in RUST expressing tabular data structures (Vec<Objects>?)

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
