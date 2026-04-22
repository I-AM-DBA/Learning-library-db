#!/usr/bin/env bash

function main()
{
    local -r LIBRARY_ARCHIVE_PATH=/docker-entrypoint-initdb.d/library-20260413.tar.gz
    local -r LIBRARY_JSON_FILENAME=20260413.json

    # attempt to create a temporary directory and exit with an error if it fails
    local tempDirectory; tempDirectory=$( mktemp -d ) || exit 1

    # extract the archive file
    echo "Extracting $LIBRARY_ARCHIVE_PATH"
    local libraryJsonPath=$tempDirectory/$LIBRARY_JSON_FILENAME
    tar -xzf $LIBRARY_ARCHIVE_PATH -C $tempDirectory
    echo "Extracted to $libraryJsonPath"

    # modify the json file to a form that postgres can import
    # - remove the first 3 lines
    # - remove the last line
    # - remove the trailing comma from the all lines
    echo "Modifying $libraryJsonPath file..."
    sed -i -e '1,3d' -e 's/,$//' -e 'N;$!P;$!D;$d' $libraryJsonPath

    psql -U postgres -d library << EOF
CREATE TEMP TABLE raw_json (data jsonb);

COPY
raw_json FROM '$libraryJsonPath'
WITH (FORMAT CSV, QUOTE e'\x01', DELIMITER e'\x02');

INSERT INTO raw_books
SELECT
    data->>'crityn',
    data->>'nbook_yn',
    data->>'lang_name',
    data->>'lang',
    data->>'sub_loca_name',
    data->>'author',
    data->>'loca_name',
    data->>'title',
    data->>'class_no',
    data->>'loan_status_name',
    data->>'create_date',
    data->>'page',
    data->>'old_intrcn_yn',
    data->>'isbn',
    data->>'onlnyn',
    data->>'publer',
    data->>'bib_type_name',
    data->>'oldyn',
    data->>'urlyn',
    data->>'contry_name',
    data->>'loca',
    data->>'loan_status',
    data->>'sub_loca',
    data->>'absyn',
    data->>'author_no',
    data->>'call_no',
    data->>'contry',
    data->>'publer_year',
    data->>'struct_yn',
    data->>'bib_type',
    data->>'ctrlno',
    data->>'vodyn',
    data->>'append_info',
    data->>'editon'
FROM raw_json;
EOF

    # clean up the temporary directory
    rm -rf $tempDirectory
}

main "$@"
