import secrets
import io
from database import executar_query

def gerar_token():
    return f"TK-{secrets.token_hex(3).upper()}"

def gerar_relatorio_txt(token):
    chamado = executar_query(
        "SELECT usuario_nome, atendente_nome, data_abertura, data_fechamento, status FROM chamados WHERE token = %s",
        (token,), fetchone=True
    )
    if not chamado:
        return None, None

    user_nome, staff_nome, dt_abertura, dt_fechamento, status = chamado
    mensagens = executar_query(
        "SELECT autor_nome, conteudo, data_envio FROM mensagens_chamados WHERE token = %s ORDER BY data_envio ASC",
        (token,), fetchall=True
    )

    relatorio = [
        "==================================================",
        f"          RELATORIO DE ATENDIMENTO - {token}",
        "==================================================",
        f"Cliente        : {user_nome}",
        f"Atendente      : {staff_nome or 'Nao assumido'}",
        f"Status         : {status}",
        f"Data Abertura  : {dt_abertura.strftime('%d/%m/%Y %H:%M:%S') if dt_abertura else 'N/A'}",
        f"Data Fechamento: {dt_fechamento.strftime('%d/%m/%Y %H:%M:%S') if dt_fechamento else 'Em aberto'}",
        "==================================================",
        "               HISTORICO DE MENSAGENS             ",
        "==================================================\n"
    ]

    if mensagens:
        for autor, conteudo, data in mensagens:
            data_str = data.strftime("%d/%m/%Y %H:%M:%S")
            relatorio.append(f"[{data_str}] {autor}: {conteudo}")
    else:
        relatorio.append("Nenhuma mensagem registrada.")

    relatorio.append("\n==================================================")
    relatorio.append("                 FIM DO RELATORIO                 ")
    relatorio.append("==================================================")

    buffer = io.BytesIO("\n".join(relatorio).encode("utf-8"))
    return buffer, f"relatorio-{token}.txt"