# README

```bash
cd /home/cb/tmp/robival/robival_data_corpus/raw
find . -type d | sort > /home/cb/work_online/data-steward/hackathon_webby_fdos/input/directory_paths.txt
find . -type f | sort > /home/cb/work_online/data-steward/hackathon_webby_fdos/input/file_paths.txt
find . -type f | sort | xargs -d '\n' stat -c "%s %n" > /home/cb/work_online/data-steward/hackathon_webby_fdos/input/file_sizes.txt
```