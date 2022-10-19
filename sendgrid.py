from typing import List, Dict
from dataclasses import dataclass

from aiohttp import ClientSession


MAIL_SUBJECT_MANAGER_NEW_COLABORATOR = "[Onboarding] Aqui está o login da nova pessoa do seu time: -fname-"
MAIL_CONTENT_MANAGER_NEW_COLABORATOR = """<head>
    <title>Enter the subject here</title>
    <style>
        <!-- body { font-family: 'Trebuchet MS'} -->
    </style>
</head>
<body bgcolor="#FFFFFF">
    <p>Olá, tudo bem?</p>
    <p>Sabemos que tem gente nova chegando para o seu time! Para te ajudar nesse período de onboarding, o time de Educação preparou um <b>material completo para te ajudar nessa recepção</b>. Nesse material você vai encontrar um checklist do que não pode faltar em um bom onboarding e diversos templates para você personalizar! Clique <a href="https://drive.google.com/drive/folders/1n2zZJWCrzvW91qEmWk3hC5q_8dmg3VPD">aqui</a> para ver mais.</p>
    <p>
        Este e-mail é para te avisar que o login e as instruções de como realizar a criação da primeira senha serão enviados diretamente para as novas pessoas <b>no primeiro dia de trabalho</b>.<br>
        Para definir a senha, o entrante receberá um token por SMS, no celular cadastrado durante as etapas de seleção. Com token em mãos terá autonomia para acessar o Portal Dory e criar sua senha.<br>
        Esse é o <b>login</b> da pessoa que está chegando para o seu time:<br>
        E-mail: -fmail-
    </p>
    <p>Mas não se preocupe, vamos enviar junto com as comunicações do Welcome essa informação para ela.</p>
    <p>
        Em caso de dúvidas ou problemas, entre em contato com o time SOS Field Services:<br>
        E-mail: sos.fieldservices@DOMAINr<br>
        Workplace: LINK DO WORKPLACE<br>
        Slack: Canal <a href="LINK DO CANAL">#sos</a><br>
    </p>
    <p>
        Telefones de contato:<br>
        São Paulo: (11)PHONE e (11)PHONE<br>
        Rio de Janeiro: (21)PHONE e (21)PHONE<br>
    </p>
</body>"""

MAIL_SUBJECT_NEW_COLABORATOR = "Seu login está aqui!"
MAIL_CONTENT_NEW_COLABORATOR = """<head>
    <title>Enter the subject here</title>
    <style>
        <!-- body { font-family: 'Trebuchet MS'} -->
    </style>
</head>
<body bgcolor="#FFFFFF">
    <p>Olá!</p>
    <p>
        Conferiu no Guia do Welcome que você iria receber seu login através do nosso e-mail?<br>
        Ele acaba de chegar! ;)
    </p>
    <p>Com o seu login corporativo, você conseguirá realizar o seu primeiro acesso às nossas plataformas e sistemas. <br>
    *** Lembramos que para este acesso é necessário estar com o celular ***</p>
    <p>
        <b>Seu e-mail corporativo: </b>-fmail-<br>
    </p>
    <p><b>Realize o procedimento (bit.ly/PassoaPasso_Enterprise) para criar sua senha e teste o seu login após a nossa live de Boas-vindas</b> e, se tiver dificuldade, responda ao formulário: LINK</p>
    <p>Até logo!</p>
</body>"""


@dataclass
class SendGrid():
    token: str

    async def send_mail(
        self,
        session: ClientSession,
        sender: str,
        subject: str,
        content: List[Dict[str, str]],
        data: dict,
    ) -> None:
        headers = {"Authorization": f"Bearer {self.token}"}
        mail_data = {"personalizations": data, "from": {"email": sender}, "subject": subject, "content": content}        
        async with session.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=mail_data) as response:
            return response
