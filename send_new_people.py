from asyncio import run, gather
from sys import argv

import pandas as pd, numpy
from aiohttp import ClientSession
from dotenv import load_dotenv

from sendgrid import SendGrid, MAIL_SUBJECT_NEW_COLABORATOR, MAIL_CONTENT_NEW_COLABORATOR


async def main():
    welcome_date = argv[1]

    # Format IDM users dataframe
    corporate_mail = pd.read_csv(
        f"welcome/{welcome_date}/welcome_{welcome_date}_pmail.csv",
        usecols=["fullName", "CPF", "mail", "mobile", "StartDate"],
        converters={"mobile": str}
    )
    corporate_mail["StartDate"] = pd.to_datetime(corporate_mail["StartDate"])
    corporate_mail["StartDate"] = [row.replace(hour=10) for row in corporate_mail["StartDate"]]
    corporate_mail["StartDate"] = corporate_mail["StartDate"].astype(numpy.int64) // 10 ** 9

    # Format personal mail dataframe
    personal_mail = pd.read_excel(
        f"welcome/{welcome_date}/novos_entrantes_{welcome_date}.xlsx", converters={"CPF": str}
    )
    personal_mail["CPF"] = [f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" for cpf in personal_mail["CPF"].str.zfill(11)]
    personal_mail.rename(columns={"E-mail Pessoal": "personal_mail"}, inplace=True)

    new_people = corporate_mail.merge(personal_mail[["CPF", "personal_mail"]], on="CPF")

    # Structure personalizations as batches of 100 mails
    batch_len = 100
    personalizations = [
        {
            "to": [
                {
                    "email": personal_mail,
                },
            ],
            "send_at": send_at,
            "substitutions": {"-fmail-": mail, "-fmobile-": mobile}
        }
        for personal_mail, send_at, mail, mobile
        in zip(new_people["personal_mail"], new_people["StartDate"], new_people["mail"], new_people["mobile"])
    ]
    personalization_batches = [personalizations[i:i + batch_len] for i in range(0, len(personalizations), batch_len)]
    print(sum(len(batch) for batch in personalization_batches))
    print(len(personalization_batches))

    # Send mails with SendGrid
    send_grid = SendGrid("SECRET")
    async with ClientSession() as session:
        responses = await gather(*[
            send_grid.send_mail(
                session,
                "educacao@.com.br",
                MAIL_SUBJECT_NEW_COLABORATOR,
                [{"type": "text/html", "value": MAIL_CONTENT_NEW_COLABORATOR}],
                data,
            )
            for data in personalization_batches
        ])
        print([r.status for r in responses])
    return "Success"


if __name__ == "__main__":
    load_dotenv()
    run(main())
