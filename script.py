import os
import dotenv
import re
import warnings

from openai import OpenAI

from utils.output import Output


dotenv.load_dotenv()

SYSTEM_CONTEXT_PATH = "context/system_context.txt"
ASSISTENT_SAMPLE_PATH = "context/assistant_output_sample.txt"
USER_SAMPLE_PATH = "context/user_input_sample.txt"


def request(system_context, input_context, user_sample, assistant_sample):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_context},
            {"role": "user", "content": user_sample},
            {"role": "assistant", "content": assistant_sample},
            {"role": "user", "content": input_context},
        ],
    )
    return response.choices[0].message.content, response.usage


def sanitize_title(task_title):
    return re.sub(r"/", "\\\\", task_title)


def read_file(file_path):
    with open(file_path) as file:
        return file.read()


def get_input_context(file_path):
    with open(file_path) as file:
        task_title = sanitize_title(file.readline().strip())
        input_context = file.read()

    return task_title, input_context


def get_file_path(task_title, output_dir):
    cwd_path = os.getcwd()

    file_path = f"{output_dir}/{task_title}"
    file_format = ".md"

    path_to_file = f"{cwd_path}{file_path}"
    if os.path.exists(path_to_file + file_format):
        i = 1
        while os.path.exists(path_to_file + f" ({i})" + file_format):
            i += 1
        return path_to_file + f" ({i})" + file_format
    return path_to_file + file_format


def create_md(task_title, output_dir):
    file_path = get_file_path(task_title, output_dir)
    was_created = False

    try:
        with open(file_path, "w") as md_file:
            was_created = True
            pass
    except FileNotFoundError:
        raise FileNotFoundError(file_path)

    return was_created, file_path


def write_md(content, file_path):
    with open(file_path, "w") as result_file:
        result_file.write(content)


def run(args):
    Output.start()
    user_input = args.input_file
    output_dir = (
        args.output_dir[:-1] if args.output_dir.endswith("/") else args.output_dir
    )
    output_dir = output_dir if output_dir.startswith("/") else f"/{output_dir}"

    if not user_input:
        warnings.warn(
            "Você precisa definir um arquivo de entrada com '--input_file [path]'"
        )
        return

    Output.create_file()
    task_title, input_context = get_input_context(user_input)
    file_created, output_path = create_md(task_title, output_dir)

    Output.prep()
    system_context = read_file(SYSTEM_CONTEXT_PATH)
    user_sample_content = read_file(USER_SAMPLE_PATH)
    assistant_sample_content = read_file(ASSISTENT_SAMPLE_PATH)

    if file_created:
        Output.request()
        md_content, usage = request(
            system_context, input_context, assistant_sample_content, user_sample_content
        )
        write_md(md_content, output_path)

        Output.success()
        Output.file_location(output_path)
        Output.costs(usage)
