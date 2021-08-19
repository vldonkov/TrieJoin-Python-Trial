datasets_dir=$1
output_dir=$2

python main_snap.py $datasets_dir $output_dir
python main_imdb.py $datasets_dir $output_dir