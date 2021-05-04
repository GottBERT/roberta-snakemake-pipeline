use std::collections::HashMap;

pub fn symbols_map(language: &str) -> HashMap<&'static str, &'static str> {
    let mut characters = HashMap::new();

    match language {
      "German" => {
        // ISO-8859-10
        characters.insert("ÃĪ", "ä");
        characters.insert("Ãž", "ü");
        characters.insert("Ãķ", "ö");
        characters.insert("Ã", "ß");
        characters.insert("Ã", "Ä");
        characters.insert("Ã", "Ü");
        characters.insert("Ã", "Ö");

        // ISO-8859-15
        characters.insert("Ã€", "ä");
        characters.insert("ÃŒ", "ü");
        characters.insert("Ã¶", "ö");
        characters.insert("Ã", "ß");
        characters.insert("Ã", "Ä");
        characters.insert("Ã", "Ü");
        characters.insert("Ã", "Ö");

        // ISO-8859-1
        characters.insert("Ã¤", "ä");
        characters.insert("Ã¼", "ü");
        characters.insert("Ã¶", "ö");
        characters.insert("Ã", "ß");
        characters.insert("Ã", "Ä");
        characters.insert("Ã", "Ü");
        characters.insert("Ã", "Ö");

        // ISO-8859-2
        characters.insert("Ă¤", "ä");
        characters.insert("Ăź", "ü");
        characters.insert("Ăś", "ö");
        characters.insert("Ă", "ß");
        characters.insert("Ă", "Ä");
        characters.insert("Ă", "Ü");
        characters.insert("Ă", "Ö");

        // ISO-8859-4
        characters.insert("Ã¤", "ä");
        characters.insert("Ãŧ", "ü");
        characters.insert("Ãļ", "ö");
        characters.insert("Ã", "ß");
        characters.insert("Ã", "Ä");
        characters.insert("Ã", "Ü");
        characters.insert("Ã", "Ö");

        // ISO-8859-9
        characters.insert("Ã¤", "ä");
        characters.insert("Ã¼", "ü");
        characters.insert("Ã¶", "ö");
        characters.insert("Ã", "ß");
        characters.insert("Ã", "Ä");
        characters.insert("Ã", "Ü");
        characters.insert("Ã", "Ö");

        // Windows-1250
        characters.insert("Ă¤", "ä");
        characters.insert("ĂĽ", "ü");
        characters.insert("Ă¶", "ö");
        characters.insert("Ăź", "ß");
        characters.insert("Ă„", "Ä");
        characters.insert("Ăś", "Ü");
        characters.insert("Ă–", "Ö");

        // Windows-1252
        characters.insert("Ã¤", "ä");
        characters.insert("Ã¼", "ü");
        characters.insert("Ã¶", "ö");
        characters.insert("ÃŸ", "ß");
        characters.insert("Ã„", "Ä");
        characters.insert("Ãœ", "Ü");
        characters.insert("Ã–", "Ö");
      },
      _ => {}
    }
    
    return characters;
}