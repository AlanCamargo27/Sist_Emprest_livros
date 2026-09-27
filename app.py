import streamlit as st
from banco import (
    criar_tabela,
    inserir_registro,
    listar_registro,
    atualizar_devolucao,
    excluir_registros
)

st.set_page_config(
    page_title="Registro de Empréstimo da Biblioteca",
    layout="wide"
)

st.title("Registro de Empréstimos da Biblioteca")

criar_tabela()

st.subheader("Registrar novo empréstimo de livro")

with st.form("form_cadastro", clear_on_submit=True):
    col_a, col_b = st.columns(2)

    with col_a:
        leitor = st.text_input("Leitor:")
        genero = st.selectbox(
            "Gênero:",
            ["Suspense", "Fantasia", "Terror", "Aventura", "Autobiografia", "Educativo", "Thriller", "Romance"],
             index=None,
             placeholder="Selecione o gênero do livro"
        )
        livro = st.selectbox(
            "Livro:",
            ["Céu e mar"],
            index=None,
            placeholder="Selecione o livro"
        )

    with col_b:
        devolucao = st.selectbox(
            "Devolvido?:",
            ["Sim", "Não"],
            index=None,
            placeholder="sim ou não"
        )
        data = st.date_input("Data do Empréstimo:", format="DD/MM/YYYY")

    enviado = st.form_submit_button("Salvar registro")

    if enviado:
        if leitor.strip() == "" or livro.strip() == "":
            st.error("Preencha todos os campos antes de salvar.")
        else:
            inserir_registro(
                leitor,
                genero,
                livro,
                devolucao,
                data.strftime("%d/%m/%Y")
            )
            st.success(f"Empréstimo para {leitor} registrado com sucesso!")
            st.rerun()

st.divider()

st.subheader("Análise automática")

df = listar_registro()

if df.empty:
    st.info(
        "Nenhum empréstimo registrado ainda. "
        "Use o formulário acima para começar."
    )
else:
    col1, col2, col3 = st.columns(3)
    total_livros_emprestados = len(df)

    col1.metric(
        "Total de livros empréstados",
        f"{total_livros_emprestados}"
    )

    grafico_leitor, grafico_genero = st.columns(2)

    with grafico_leitor:
        st.write("**Total De livros por leitor**")
        total_por_leitor = df.groupby("leitor")["id"].sum()
        st.bar_chart(total_por_leitor,horizontal=True)

    with grafico_genero:
        st.write("**Total por gênero**")
        total_por_genero = df.groupby("genero")["id"].count()
        st.bar_chart(total_por_genero)

    st.subheader("Todos os empréstimos registrados")
    st.dataframe(df, use_container_width=True)

   
    with st.expander("Marcar livro como devolvido"):
        pendentes = df[df["devolucao"] == "Não"]
        if pendentes.empty:
            st.success("Não há empréstimos pendentes no momento!")
        else:
            opcoes = {
                f"ID {row['id']} - {row['leitor']} ({row['livro']})": row['id']
                for _, row in pendentes.iterrows()
            }
            selecionado = st.selectbox(
                "Selecione o empréstimo para registrar devolução:",
                options=list(opcoes.keys())
            )
            if st.button("Marcar como devolvido"):
                id_selecionado = opcoes[selecionado]
                atualizar_devolucao(id_selecionado, "Sim")
                st.success(f"Empréstimo ID {id_selecionado} atualizado para 'Devolvido'!")
                st.rerun()

    
    with st.expander("Excluir registos"):
       registros_df = df

       if registros_df.empty:
        st.info("Não há empréstimos registrados para excluir!")

       else:
        opcoes_registros = {
            f"ID {row['id']} - {row['leitor']} ({row['livro']})": row['id']
            for _, row in registros_df.iterrows()
        }

        selecionados = st.multiselect(
            "Selecione um ou mais registos para excluir:",
            options=list(opcoes_registros.keys()), 
            placeholder="Escolha os registos para excluir..."
        )

        if st.button("Excluir Seleção"):
            if selecionados:
                
                for item in selecionados:
                    id_para_excluir = opcoes_registros[item]
                    excluir_registros(id_para_excluir)
                
                st.success(f"{len(selecionados)} registo(s) excluído(s) com sucesso.")
                st.rerun()
            else:
                st.warning("Por favor, selecione pelo menos um registo antes de clicar em Excluir.")