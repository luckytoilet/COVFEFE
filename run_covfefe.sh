# testing lex features
#python covfefe.py -i ~/research/lex_test -o ~/research/lex_out -p multilingual_lex -n 1
#python covfefe.py -i ~/research/lex_test -o ~/research/lex_out -p lex

# dementiabank
#python covfefe.py -i ~/data/dementiabank_txt/Controls -o ~/research/dementiabank_features/Controls -p lex -n 16
#python covfefe.py -i ~/data/dementiabank_txt/Dementia -o ~/research/dementiabank_features/Dementia -p lex -n 16

# lu extracted narrations (chinese)
#python covfefe.py -i ~/research/bai-alzheimer/derived_data/lu_extracted_narration -o ~/data/mandarin_features -p multilingual_lex -n 1

# google translated mandarin
#python covfefe.py -i ~/research/bai-alzheimer/data/lu_google_translated/ -o ~/data/mandarin_translated_features/ -p lex -n 16

# opensubtitles pieces
python covfefe.py -i /h/bai/moar/os_narrations_en/ -o /h/bai/moar/os_features_en/ -p lex -n 16
#python covfefe.py -i /h/bai/moar/os_narrations_zh/ -o /h/bai/moar/os_features_zh/ -p multilingual_lex -n 1
