import argparse
import os
import dotenv
import warnings

from openai import OpenAI


dotenv.load_dotenv()

SYSTEM_CONTEXT_PATH = 'context/system_context.txt'
ASSISTENT_SAMPLE_PATH = 'context/assistant_output_sample.txt'
USER_SAMPLE_PATH = 'context/user_input_sample.txt'


def parse_args():
    parser = argparse.ArgumentParser(
        description='Script para gerar cenários de testes utilizando a IA da OpeinAI')
    parser.add_argument('--input_file', '-i', type=str,
                        help='Caminho do arquivo de input contendo os detalhes da task')
    parser.add_argument('--output_dir', '-o', type=str,
                        default='./', help='Caminho de destino do diretório')

    return parser.parse_args()


def request(system_context, input_context, user_sample, assistant_sample):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_context},
            {"role": "user", "content": user_sample},
            {"role": "assistant", "content": assistant_sample},
            {"role": "user", "content": input_context}
        ]
    )
    print(response.usage)
    return response.choices[0].message.content


def write_md(content, task_title, output_dir):
    with open(f'{output_dir}/{task_title}.md', 'w') as result_file:
        result_file.write(content)


def main():
    args = parse_args()
    user_input = args.input_file
    output_dir = args.output_dir[:-1] if args.output_dir.endswith('/') else args.output_dir

    if not user_input:
        warnings.warn(
            "Você precisa definir um arquivo de entrada com '--input_file [path]'")
        return

    with open(SYSTEM_CONTEXT_PATH) as system_file:
        system_context = system_file.read()

    with open(user_input) as input_file:
        task_title = input_file.readline().strip()
        input_context = input_file.read()

    with open(USER_SAMPLE_PATH) as user_sample_file:
        user_sample_content = user_sample_file.read()

    with open(ASSISTENT_SAMPLE_PATH) as assistant_sample_file:
        assistant_sample_content = assistant_sample_file.read()

    md_content = request(system_context,
                         input_context,
                         assistant_sample_content,
                         user_sample_content)
    write_md(md_content, task_title, output_dir)


if __name__ == '__main__':
    main()
