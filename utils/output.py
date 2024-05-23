class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CHECK_MARK = '\u2713\u2713\u2713'


PREFIX = f'{colors.BOLD}{colors.OKBLUE}[QA]{colors.ENDC}'

class Output:
    @staticmethod
    def start():
        print(f'\n{colors.BOLD}{colors.OKCYAN}#### QA Automation ####{colors.ENDC}\n')

    @staticmethod
    def create_file():
        print(f'{PREFIX} {colors.BOLD}Criando arquivo markdown...{colors.ENDC}')

    @staticmethod
    def prep():
        print(f'{PREFIX} {colors.BOLD}Preparando contexto...{colors.ENDC}')

    @staticmethod
    def request():
        print(f'{PREFIX} {colors.BOLD}Fazendo requisição para a OpenAI...{colors.ENDC}'
               f'\n     Por favor, aguarde enquanto recebemos a resposta do LLM.\n')

    @staticmethod
    def success():
        print(f'{PREFIX} {colors.BOLD}{colors.OKGREEN}Automação concluída!{colors.ENDC}')

    @staticmethod
    def file_location(file_path):
        print(f'{PREFIX} {colors.BOLD}Arquivo disponível em:{colors.ENDC} {file_path}')

    @staticmethod
    def costs(usage):
        completion_tokens = usage.completion_tokens
        prompt_tokens = usage.prompt_tokens
        total_tokens = usage.total_tokens
        print(f'\n{colors.BOLD}{colors.WARNING}+++ CUSTOS +++{colors.ENDC}')
        print(f'Completion tokens: {colors.BOLD}{completion_tokens}{colors.ENDC}')
        print(f'Prompt tokens: {colors.BOLD}{prompt_tokens}{colors.ENDC}')
        print(f'Total tokens: {colors.BOLD}{total_tokens}{colors.ENDC}')
