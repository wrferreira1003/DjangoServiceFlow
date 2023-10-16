# DjangoServiceFlow

O projeto DjangoServiceFlow é uma aplicação Django projetada para ser hospedada em uma VPS da Hostinger.

---

## Índice

- [Configuração](#configuração)
- [Desenvolvimento e Workflow](#desenvolvimento-e-workflow)
- [Conclusão](#conclusão)

---

## Configuração

### Arquivo .env
As configurações sensíveis e variáveis ​​de ambiente específicas são armazenadas no arquivo `.env`. Este arquivo não deve ser comitado no repositório por razões de segurança. Ele contém informações como chaves secretas, credenciais de banco de dados e configurações de email.

### Branch Main (Produção)
A branch `main` no repositório Git serve como a fonte de verdade para o ambiente de produção. Somente código completamente testado e revisado deve ser mesclado nesta branch. Esta é a branch que está conectada e é implantada na VPS da Hostinger.

---

## Desenvolvimento e Workflow

### Ambiente de Desenvolvimento
Foi criada uma branch separada chamada `development`. Esta branch é onde todo o desenvolvimento ativo ocorre. Novas funcionalidades, correções de bugs e melhorias são feitas nesta branch ou em branches derivadas dela.

### Pull Requests
Ao concluir o desenvolvimento de uma feature ou correção em uma branch de desenvolvimento, um Pull Request (PR) deve ser criado para mesclar essas mudanças na branch `main`. O PR serve como uma oportunidade para revisar as alterações, discutir implementações e garantir que todos os testes passem antes da mesclagem.

### Testes
Antes de mesclar qualquer alteração na branch `main`, é imperativo que todas as funcionalidades sejam devidamente testadas para garantir que não introduzam novos bugs ou quebrem funcionalidades existentes.

### Atualizações no Ambiente de Produção
Uma vez que as alterações na branch de desenvolvimento tenham sido revisadas e testadas, elas podem ser mescladas na branch `main` e, em seguida, implantadas na VPS da Hostinger.

---

## Conclusão

O projeto DjangoServiceFlow segue um workflow estruturado para garantir a integridade e a segurança do código em produção. Ao aderir a esta estrutura e documentação, asseguramos que o projeto permanecerá sustentável, escalável e fácil de gerenciar à medida que cresce e evolui.

**Nota**: Esta é uma documentação inicial e será atualizada e expandida conforme o projeto avança.
