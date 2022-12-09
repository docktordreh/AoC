#!/usr/bin/env sh
infile=day7.txt
set --
size=0
while IFS= read -r line; do
    set -- "$@" "$line;"
    size=$((size+1))
done <"$infile"
dirs=""
line_visited=""


visitDir() {
    local cur_line
    local linecounter
    local size
    local tmparr
    local cur_dir
    local cur_dir_size
    local nest
    linecounter="$(echo "$@" | awk -F '|' '{print $1}')"
    size="$(echo "$@" | awk -F '|' '{print $2}')"
    tmparr="$(echo "$@" | awk -F '|' '{print $3}')"
    set --
    OIFS=$IFS
    IFS=";"
    for l in $tmparr; do
          set -- "$@" "$l;"
    done
    IFS=$OIFS

    cur_dir_size=0
    cur_dir="/"
    prev_line=$((linecounter-1))
    prev_line="$(eval "echo \${${prev_line}}")"
    cur_dir="$(echo "$prev_line" | sed -e 's#\$ cd ##' -e 's#;##g')"
    case "$cur_dir" in
        "$0")
            cur_dir="/";;

            *);;
    esac


    nest=1
    for i in $(seq $((linecounter)) $((size+1))); do
        cur_line="$(eval "echo \${${i}}")"
        # echo "LINE $cur_line"
        if test "${line_visited#*"$cur_line"}" != "$line_visited"; then
            case "$cur_line" in
                *" cd .."*) ;;
                *)
                    #echo "skipping line $cur_line";
                    continue ;;
            esac
        fi
        line_visited="$line_visited $cur_line"
        case $cur_line in
            "$ cd "[A-z]*)
                # echo "MATCH cd [A-z]*"
                next_dir="$(echo "$cur_line" | sed -e 's#\$ cd ##' -e 's#;##g')"
                # echo "visiting dir $next_dir"
                nest=$((nest+1))
                visitDir "$((i+1))|$size|$@"
                cur_dir_size=$((cur_dir_size+$?))
                # echo "--> cur size of $cur_dir $((cur_dir_size))"
                ;;
            "$ cd .."*)
                # echo "MATCH cd ..*"
                nest=$((nest-1))
                if [ $nest -le 0 ]; then
                    case "$cur_dir" in
                        "/")
                            continue
                            ;;
                        *)
                            # echo "--> backtracking from $cur_dir calculated size $cur_dir_size for $cur_dir"
                            dirs="$dirs\n$cur_dir $cur_dir_size"
                            return $cur_dir_size
                            ;;
                    esac
                fi
                ;;
            "$ cd /"*)
                # echo "MATCH: $cur_line cd root"
                ;;
            *"dir"*)
                # echo "MATCH dir: $cur_line has a dir, handling later"
                ;;
            *"ls;") # echo "MATCH *ls; $cur_line listing files"
                ;;
            *)
                local s
                s="$(echo "$cur_line" | awk -F ' ' '{print $1}')"
                cur_dir_size=$((cur_dir_size+s))
                # echo "--> file of size $s in $cur_dir, cur size of $cur_dir $((cur_dir_size))"
                ;;
        esac
    done
    dirs="$dirs\n$cur_dir $cur_dir_size"
    # echo "--> calculated size $cur_dir_size for $cur_dir"
    return $cur_dir_size
}
result1=0
# posix arrays start at 1
visitDir "1|$size|$@"
echo "$dirs"
IFS="\n"
for dir in $dirs; do
    [ -z "$dir" ] && continue
    echo "$dir"
    num="$(echo "$dir" | awk -F ' ' '{print $2}' | sed 's#\n##g')"
    if [ "$num" -le 100000 ]; then result1=$((result1+num)); fi
done



echo "result 1: $result1"
