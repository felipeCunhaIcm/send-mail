from asyncio import run, gather
from os import environ
from sys import argv

import pandas as pd
from aiohttp import ClientSession
from dotenv import load_dotenv

from sendgrid import SendGrid, MAIL_SUBJECT_MANAGER_NEW_COLABORATOR, MAIL_CONTENT_MANAGER_NEW_COLABORATOR


async def main():
    welcome_date = argv[1]

    # Load dataframes
    base_file_path = f"welcome/{welcome_date}/welcome_{welcome_date}"
    new_people = pd.read_csv(f"{base_file_path}_pmail.csv", usecols=["CPF", "fullName", "mail", "managerCPF", "BPCPF"])

    manager = pd.read_csv(f"{base_file_path}_manager.csv")
    manager = manager.loc[manager["employeeStatus"] == "ATIVO"].drop_duplicates("CPF").reset_index(drop=True)

    bp = pd.read_csv(f"{base_file_path}_bp.csv")
    bp = bp.loc[bp["employeeStatus"] == "ATIVO"].drop_duplicates("CPF").reset_index(drop=True)

    # Merge and format dataframes
    new_people = new_people.merge(
        bp[["CPF", "mail"]], how="left", left_on="BPCPF", right_on="CPF", suffixes=["", "_bp"]
    )
    new_people = new_people.merge(
        manager[["CPF", "mail"]], how="left", left_on="managerCPF", right_on="CPF", suffixes=["", "_manager"]
    )
    new_people = new_people.drop(columns=["CPF_bp", "CPF_manager"]).fillna("")

    # Structure personalizations as batches of 100 mails
    batch_len = 100
    personalizations = [
        {
            "to": [
                {
                    "email": mail_manager if mail_manager else "sos.acessos@stone.com.br",
                },
                {
                    "email": mail_bp if mail_bp and mail_bp != mail_manager else "admissao@stone.com.br",
                },
            ],
            "bcc": [{"email": "onboarding@stone.com.br"}],
            "substitutions": {"-fname-": name, "-fmail-": mail}
        }
        for name, mail, mail_manager, mail_bp
        in zip(new_people["fullName"], new_people["mail"], new_people["mail_manager"], new_people["mail_bp"])
    ]
    personalization_batches = [personalizations[i:i + batch_len] for i in range(0, len(personalizations), batch_len)]
    print(sum(len(batch) for batch in personalization_batches))
    print(len(personalization_batches))

    # Send mails with SendGrid
    send_grid = SendGrid(environ["send_grid_token"])
    async with ClientSession() as session:
        responses = await gather(*[
            send_grid.send_mail(
                session,
                "iam@stone.com.br",
                MAIL_SUBJECT_MANAGER_NEW_COLABORATOR,
                [{"type": "text/html", "value": MAIL_CONTENT_MANAGER_NEW_COLABORATOR}],
                data,
            )
            for data in personalization_batches
        ])
        print([r for r in responses])


if __name__ == "__main__":
    load_dotenv()
    run(main())
