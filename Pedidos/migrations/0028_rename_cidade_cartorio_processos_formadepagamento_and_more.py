# Generated by Django 4.2.3 on 2023-11-26 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0027_rename_cpf_processos_cpf_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processos',
            old_name='Cidade_Cartorio',
            new_name='FormaDePagamento',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Registro_Geral',
            new_name='RegistroGeral',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Registro_Geral_Envolvido',
            new_name='RegistroGeralEnvolvido',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Cep',
            new_name='cep',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Conjugue_1',
            new_name='cidadeCartorio',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Conjugue_2',
            new_name='conjugue1',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Estado_Cartorio',
            new_name='conjugue2',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='CPF',
            new_name='cpf',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='CPF_Envolvido',
            new_name='cpfEnvolvido',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Data_Casamento',
            new_name='data_casamento',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Data_Final',
            new_name='data_final',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Data_Inicial',
            new_name='data_inicial',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Data_Nascimento',
            new_name='data_nascimento',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Data_Obito',
            new_name='data_obito',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Endereco',
            new_name='endereco',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Estado',
            new_name='estado',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Estado_Cartorio_Firma_Reconhecida',
            new_name='estadoCartorio',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Filiacao_1',
            new_name='estadoCartorioFirmaReconhecida',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Estado_Civil',
            new_name='estado_civil',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Filho_Incapaz',
            new_name='filhoIncapaz',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Filiacao_2',
            new_name='filiacao1',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Folha_Cartorio',
            new_name='filiacao2',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Forma_De_Pagamento',
            new_name='folhaCartorio',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Livro_Cartorio',
            new_name='livroCartorio',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Livro_Cartorio_Firma_Reconhecida',
            new_name='livroCartorioFirmaReconhecida',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Nome',
            new_name='nome',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Nome_Cartorio',
            new_name='nomeCartorio',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Nome_Cartorio_Firma_Reconhecida',
            new_name='nomeCartorioFirmaReconhecida',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Nome_Envolvido',
            new_name='nomeEnvolvido',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Nome_Falecido',
            new_name='nome_falecido',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Profissao',
            new_name='profissao',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Sobrenome_Envolvido',
            new_name='sobrenomeEnvolvido',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Status',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Telefone',
            new_name='telefone',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Tem_Bens',
            new_name='temBens',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Tem_Filhos_Menores',
            new_name='temFilhosMenores',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Termo',
            new_name='termo',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='Tipo_De_Entrega',
            new_name='tipoDeEntrega',
        ),
    ]
