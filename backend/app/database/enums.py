from enum import Enum


class Role(str, Enum):
    admin = 'admin'
    user = 'user'


class PedidoStatus(str, Enum):
    pendente = 'pedido criado, mas não confirmado pelo cliente'
    confirmado = 'pedido confirmado pelo usuario e validado pelo sistema'
    enviado = 'pedido enviado para o cliente'
    entregue = 'pedido entregue ao cliente'
    cancelado = 'pedido cancelado pelo cliente'
    devolvido = 'pedido devolvido após a entrega'