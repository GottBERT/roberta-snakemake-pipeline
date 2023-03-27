extern crate natural;

use natural::tokenize::tokenize;

use std::{
    fs::File,
    io::{prelude::*, BufReader},
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
    // read stopwords
    let stop_words = lines_from_file("/home/scheible/git/lrz/NLP/BERT/GottBERT/workflow_filterdata/scripts/compute_ratios/src/stopwords/german");


    // TODO: here will come some loop over a file reading each line
    let document = String::from("Hello, wollte world world world!");

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
    let num_punctuation = non_word_token.len();

    let mut tokens : Vec<String> = Vec::from(word_tokens.to_vec());
    tokens.append(&mut non_word_token);

    // number of tokens of the original document
    let num_tokens_original = tokens.len();

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
    let num_upper = upper_word_token.len();

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
    
    let num_unique_tokens_filtered = filtered_tokens.into_iter().unique_n();

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

    println!("stopword_ratio: {:?}", stopword_ratio);
    println!("punctuation_ratio: {:?}", punctuation_ratio);
    println!("#tokens_original: {:?}", num_tokens_original);
    println!("#tokens_filtered: {:?}", num_unique_tokens_filtered);
    println!("#tokens_puctuation: {:?}", num_punctuation);
    println!("token_ratio: {:?}", token_ratio);
    println!("#token_upper: {:?}", num_punctuation);
    println!("upper_ratio: {:?}", upper_ratio);
    println!("upper_to_punct_ratio: {:?}", upper_to_punct_ratio);

}
