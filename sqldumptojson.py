import json
from pathlib import Path
from typing import Annotated

import typer
from rich.progress import open as open_rich
from sqloxide import parse_sql

app = typer.Typer()


def _build_final_dict(desired, field_index, final_dict, row):
    final_value = row[field_index[desired]]["Value"]
    if "SingleQuotedString" in final_value:
        final_value = final_value["SingleQuotedString"]

    elif "Number" in final_value:
        final_value = final_value["Number"][0]
    final_dict[desired] = final_value


def _parse_dump(dump_filename, target_table, output_directory):
    with open_rich(dump_filename, "r") as f:
        desired_fields = [
            "ID",
            "Title",
            "Author",
            "Year",
            "Identifier",
            "Filesize",
            "Extension",
            "MD5",
        ]

        statement_counter = 0

        for line in f:
            try:
                parser = parse_sql(line, dialect="mysql")
            except ValueError:
                continue

            field_index = {}

            if len(parser) > 0:
                for statement in parser:
                    if type(statement) is dict:
                        for key, val in statement.items():
                            if (
                                key == "Insert"
                                and val["table_name"][0]["value"]
                                == target_table
                            ):
                                statement_counter += 1

                                # create an index of the fields once on the
                                # first time. Assume it is the same from then
                                # onwards
                                if len(field_index) == 0:
                                    for item in val["columns"]:
                                        if item["value"] in desired_fields:
                                            field_index[item["value"]] = val[
                                                "columns"
                                            ].index(item)

                                all_results = []

                                for row in val["source"]["body"]["Values"][
                                    "rows"
                                ]:
                                    final_dict = {}

                                    for desired in desired_fields:
                                        _build_final_dict(
                                            desired,
                                            field_index,
                                            final_dict,
                                            row,
                                        )

                                    all_results.append(final_dict)

                                with open(
                                    Path(output_directory)
                                    / f"{statement_counter}.json",
                                    "w",
                                ) as output:
                                    output.write(
                                        json.dumps(
                                            all_results, ensure_ascii=False
                                        )
                                    )

    return


@app.command()
def parse(
    file: Annotated[
        str, typer.Argument(help="The input SQL dump file to parse")
    ],
    table: Annotated[
        str, typer.Argument(help="The SQL table file to recreate")
    ],
    output_directory: Annotated[
        str, typer.Argument(help="The output directory for the JSON files")
    ] = "output",
):
    """
    Convert a SQL dump to JSON files
    """
    # test whether the output directory exists and create it if not
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    _parse_dump(
        dump_filename=file,
        target_table=table,
        output_directory=output_directory,
    )


if __name__ == "__main__":
    app()
