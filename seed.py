import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal, nosql_db
from app import models

# Listas para gerar dados aleatórios verossímeis
CATEGORIAS = {
    "Eletrônicos": [
        "iPhone 15",
        "Teclado Mecânico",
        "Monitor 144hz",
        "Mouse Gamer",
        "Notebook Dell",
    ],
    "Móveis": [
        "Cadeira Office",
        "Mesa Rebatível",
        "Estante de Livros",
        "Sofá 3 Lugares",
    ],
    "Software": ["Licença Windows", "Assinatura Adobe", "Curso de Python", "Antivírus"],
    "Hardware": ["Placa de Vídeo", "Memória RAM 16GB", "SSD NVMe 1TB", "Fonte 600W"],
}

COMENTARIOS = [
    "Cliente satisfeito com a entrega rápida.",
    "Produto com excelente custo-benefício.",
    "Solicitou suporte para instalação.",
    "Aproveitou a promoção da semana.",
    "Venda via indicação de outro cliente.",
    None,  # Representa vendas sem comentário
]


def run_seed(quantidade=30):
    db: Session = SessionLocal()

    try:
        # VERIFICAÇÃO: Só roda se a tabela de vendas estiver vazia
        vendas_existentes = db.query(models.Sale).count()

        if vendas_existentes == 0:
            print(
                f"🌱 Banco vazio detectado. Gerando {quantidade} entradas aleatórias..."
            )

            for _ in range(quantidade):
                # 1. Escolha aleatória
                cat = random.choice(list(CATEGORIAS.keys()))
                prod = random.choice(CATEGORIAS[cat])

                # 2. Dados financeiros e data
                qtd = random.randint(1, 5)
                preco = round(random.uniform(100.0, 4500.0), 2)
                data = datetime.now() - timedelta(days=random.randint(0, 30))

                # 3. Salva no Postgres
                nova_venda = models.Sale(
                    product_name=prod,
                    category=cat,
                    quantity=qtd,
                    unit_price=preco,
                    created_at=data,
                )
                db.add(nova_venda)
                db.commit()  # Commit aqui para gerar o ID para o Mongo

                # 4. Salva no Mongo (Comentário Aleatório)
                txt_comentario = random.choice(COMENTARIOS)
                if txt_comentario:
                    nosql_db.comments.insert_one(
                        {"sale_id": nova_venda.id, "comment": txt_comentario}
                    )

            print(f"✅ Seed concluído! {quantidade} registros criados.")
        else:
            print(
                f"ℹ️ O banco já possui {vendas_existentes} registros. Pulando seed para preservar os dados."
            )

    except Exception as e:
        print(f"❌ Erro ao semear dados: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    run_seed(500)
