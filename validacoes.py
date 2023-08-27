from rest_framework import serializers
import os
#Validacao do arquivo, tipos de arquivos aceito
def validate_file_type(value):
    # Lista das extensões de arquivo permitidas
    valid_extensions = ['.pdf', '.doc', '.docx']
    ext = os.path.splitext(value.name)[1]  # obtem a extensão do arquivo
    if ext.lower() not in valid_extensions:
        raise serializers.ValidationError('Arquivo não suportado. Somente PDF, DOC, DOCX são permitidos.')

#Validacao do tamanho do aqrquivo
def validate_file_size(value):
    filesize = value.size
    if filesize > 1048576 * 5:  # ou o limite que você deseja definir em bytes. 1048576 bytes é 1MB
        raise serializers.ValidationError('O tamanho máximo permitido do arquivo é 1MB')