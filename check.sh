answer_dir=$1
model_answer_dir=$2


all_ok=true

# snap
if cmp -s $answer_dir/snap/facebook-1-path-count.txt $model_answer_dir/snap/facebook-1-path-count.txt; then echo '### Test Passed: facebook-1-path-count ###'; else echo '### Test Not Passed: facebook-1-path-count ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/facebook-1-path-full.txt $model_answer_dir/snap/facebook-1-path-full.txt; then echo '### Test Passed: facebook-1-path-full ###'; else echo '### Test Not Passed: facebook-1-path-full ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/facebook-2-path-count.txt $model_answer_dir/snap/facebook-2-path-count.txt; then echo '### Test Passed: facebook-2-path-count ###'; else echo '### Test Not Passed: facebook-2-path-count ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/facebook-2-path-full.txt $model_answer_dir/snap/facebook-2-path-full.txt; then echo '### Test Passed: facebook-2-path-full ###'; else echo '### Test Not Passed: facebook-2-path-full ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/facebook-triangle-count.txt $model_answer_dir/snap/facebook-triangle-count.txt; then echo '### Test Passed: facebook-triangle-count ###'; else echo '### Test Not Passed: facebook-triangle-count ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/facebook-triangle-full.txt $model_answer_dir/snap/facebook-triangle-full.txt; then echo '### Test Passed: facebook-triangle-full ###'; else echo '### Test Not Passed: facebook-triangle-full ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/twitter-1-path-count.txt $model_answer_dir/snap/twitter-1-path-count.txt; then echo '### Test Passed: twitter-1-path-count ###'; else echo '### Test Not Passed: twitter-1-path-count ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/twitter-1-path-full.txt $model_answer_dir/snap/twitter-1-path-full.txt; then echo '### Test Passed: twitter-1-path-full ###'; else echo '### Test Not Passed: twitter-1-path-full ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/twitter-2-path-count.txt $model_answer_dir/snap/twitter-2-path-count.txt; then echo '### Test Passed: twitter-2-path-count ###'; else echo '### Test Not Passed: twitter-2-path-count ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/twitter-2-path-full.txt $model_answer_dir/snap/twitter-2-path-full.txt; then echo '### Test Passed: twitter-2-path-full ###'; else echo '### Test Not Passed: twitter-2-path-full ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/twitter-triangle-count.txt $model_answer_dir/snap/twitter-triangle-count.txt; then echo '### Test Passed: twitter-triangle-count ###'; else echo '### Test Not Passed: twitter-triangle-count ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/twitter-triangle-full.txt $model_answer_dir/snap/twitter-triangle-full.txt; then echo '### Test Passed: twitter-triangle-full ###'; else echo '### Test Not Passed: twitter-triangle-full ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/wiki-1-path-count.txt $model_answer_dir/snap/wiki-1-path-count.txt; then echo '### Test Passed: wiki-1-path-count ###'; else echo '### Test Not Passed: wiki-1-path-count ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/wiki-1-path-full.txt $model_answer_dir/snap/wiki-1-path-full.txt; then echo '### Test Passed: wiki-1-path-full ###'; else echo '### Test Not Passed: wiki-1-path-full ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/wiki-2-path-count.txt $model_answer_dir/snap/wiki-2-path-count.txt; then echo '### Test Passed: wiki-2-path-count ###'; else echo '### Test Not Passed: wiki-2-path-count ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/wiki-2-path-full.txt $model_answer_dir/snap/wiki-2-path-full.txt; then echo '### Test Passed: wiki-2-path-full ###'; else echo '### Test Not Passed: wiki-2-path-full ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/wiki-triangle-count.txt $model_answer_dir/snap/wiki-triangle-count.txt; then echo '### Test Passed: wiki-triangle-count ###'; else echo '### Test Not Passed: wiki-triangle-count ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/wiki-triangle-full.txt $model_answer_dir/snap/wiki-triangle-full.txt; then echo '### Test Passed: wiki-triangle-full ###'; else echo '### Test Not Passed: wiki-triangle-full ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/enron-1-path-count.txt $model_answer_dir/snap/enron-1-path-count.txt; then echo '### Test Passed: enron-1-path-count ###'; else echo '### Test Not Passed: enron-1-path-count ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/enron-1-path-full.txt $model_answer_dir/snap/enron-1-path-full.txt; then echo '### Test Passed: enron-1-path-full ###'; else echo '### Test Not Passed: enron-1-path-full ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/enron-2-path-count.txt $model_answer_dir/snap/enron-2-path-count.txt; then echo '### Test Passed: enron-2-path-count ###'; else echo '### Test Not Passed: enron-2-path-count ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/enron-2-path-full.txt $model_answer_dir/snap/enron-2-path-full.txt; then echo '### Test Passed: enron-2-path-full ###'; else echo '### Test Not Passed: enron-2-path-full ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/enron-triangle-count.txt $model_answer_dir/snap/enron-triangle-count.txt; then echo '### Test Passed: enron-triangle-count ###'; else echo '### Test Not Passed: enron-triangle-count ###'; all_ok=false; fi
if cmp -s $answer_dir/snap/enron-triangle-full.txt $model_answer_dir/snap/enron-triangle-full.txt; then echo '### Test Passed: enron-triangle-full ###'; else echo '### Test Not Passed: enron-triangle-full ###'; all_ok=false; fi


# imdb
if cmp -s $answer_dir/imdb/query1.txt $model_answer_dir/imdb/query1.txt; then echo '### Test Passed: IMDB query1 ###'; else echo '### Test Not Passed: IMDB query1 ###'; all_ok=false; fi
if cmp -s $answer_dir/imdb/query2.txt $model_answer_dir/imdb/query2.txt; then echo '### Test Passed: IMDB query2 ###'; else echo '### Test Not Passed: IMDB query2 ###'; all_ok=false; fi
if cmp -s $answer_dir/imdb/query3.txt $model_answer_dir/imdb/query3.txt; then echo '### Test Passed: IMDB query3 ###'; else echo '### Test Not Passed: IMDB query3 ###'; all_ok=false; fi
if cmp -s $answer_dir/imdb/query4.txt $model_answer_dir/imdb/query4.txt; then echo '### Test Passed: IMDB query4 ###'; else echo '### Test Not Passed: IMDB query4 ###'; all_ok=false; fi
if cmp -s $answer_dir/imdb/query5.txt $model_answer_dir/imdb/query5.txt; then echo '### Test Passed: IMDB query5 ###'; else echo '### Test Not Passed: IMDB query5 ###'; all_ok=false; fi


if $all_ok; then
    echo '### All tests passed! ###'
else
    echo '### Error found! ###'
fi

