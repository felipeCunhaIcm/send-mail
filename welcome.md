# Welcome

Create virtualenv with required packages listed in **requirements.txt** and follow steps

## Steps to run **send_new_people.py**:
- Open Apache Directory Studio
- Login to IDM's  Tree (eDirectory)
- Execute query to get list of users for that Welcome: **(&(StartDate>={%Y%m%d}000000Z)(StartDate<={%Y%m%d}235959Z))**, where date is such as 20210802 for year, month and day
- Desired fields are: **fullName, CPF, NetworkAccount, mail, employeeStatus, StartDate, managerCPF, BPCPF, mobile, carLicense**
- Export data to CSV file named **welcome_{%Y-%m-%d}.csv**
- Onboarding team will provide a list with all personal emails of newcomers. Make sure that CPF column has header **CPF** and personal email column has header **E-mail Pessoal**, both case sensitive
- Rename XLSX file to **novos_entrantes_{%Y-%m-%d}.xlsx**
- Run script with parameter **{%Y-%m-%d}** being the desired welcome date

## Steps to run **send_bp_manager.py**
- Open Apache Directory Studio
- Login to IDM's  Tree (eDirectory)
- Execute query to get list of managers for that Welcome: **(&(|(CPF=...)(CPF=...)(CPF=...)))** with each CPF belonging to a manager of a newcomer
- Desired fields are: **CPF, mail, employeeStatus**
- Export data to CSV file named **welcome_{%Y-%m-%d}_manager.csv**
- Repeat process for list of BP's CPFs. Export data to CSV file named **welcome_{%Y-%m-%d}_bp.csv**
- Run script with parameter **{%Y-%m-%d}** being the desired welcome date