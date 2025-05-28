from enum import Enum


class Role(str, Enum):
    """O nível de acesso de um usuário no sistema.

    admins possuem acesso total e users possuem acesso limitado as rotas.


    """

    admin = 'admin'
    user = 'user'

class PedidoStatus(str, Enum):
    pendente = 'pedido criado, mas não confirmado pelo cliente'
    confirmado = 'pedido confirmado pelo usuario e validado pelo sistema'
    enviado = 'pedido enviado para o cliente'
    entregue = 'pedido entregue ao cliente'
    cancelado = 'pedido cancelado pelo cliente'
    devolvido = 'pedido devolvido após a entrega'
