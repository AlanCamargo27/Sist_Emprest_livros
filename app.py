import streamlit as st

from banco import criar_tabela, inserir_registro, listar_registro, excluir_registros

st.set_page_config(
    page_title="Sistema de Empréstimo de Livros",
    layout="wide"
)

st.title("Sistema de Empréstimo de Livros")

criar_tabela()


st.subheader("Registrar Novo Empréstimo de Livro")

with st.form("form_cadastro", clear_on_submit=True):

    col_a, col_b = st.columns(2)



    with col_a:
       


        leitor = st.text_input("Leitor:")
   

        genero = st.selectbox(
            "Gênero:",
            ["Suspense", "Fantasia", "Terror", "Aventura", "Autobiografia", "Educativo", "Thriller", "Romance"]
        )



        livro = st.selectbox(
            
            "Livro:",
            ["Céu e mar"]
            )
 

    with col_b:

       
        devolucao = st.selectbox(
            "Devolvido?:",
            ["Sim","Não"]
        )

        data = st.date_input("Data do Empréstimo:")

 
       
    enviado = st.form_submit_button("Salvar Registro")


    if enviado:
   

        if leitor.strip() == "" or livro.strip() == "":
     
            st.error("Preencha o leitor e o livro antes de salvar.")
            # Exibe uma mensagem de erro para o usuário.


        else:
            # Se vendedor e produto estiverem preenchidos,
            # executa o cadastro.


            inserir_registro(
                leitor,
                genero,
                livro,
                devolucao,
                str(data)
            )

            st.success(f"Empréstimo para { leitor} registrado com sucesso!")


            st.rerun()


st.divider()


st.subheader(" Análise automática")


df = listar_registro()


if len(df) == 0:
   

    st.info(
        "Nenhum empréstimo registrado ainda. "
        "Use o formulário acima para começar."
    )

else:

    col1, col2, col3 = st.columns(3)
   
    total_livros_emprestados = df["id"].count
 
    total_livros_emprestados = len(df)


    col1.metric(
        "Total de Livros Empréstados",
        f"{total_livros_emprestados:.2f}"
    )

    grafico_leitor, grafico_genero = st.columns(2)


    with grafico_leitor:

        st.write("**Total por Leitor**")
   
        total_por_leitor = df.groupby("leitor")["id"].value_counts

        st.bar_chart(total_por_leitor)

    with grafico_genero:
     
        st.write("**Total por Genero**")


        total_por_genero = df.groupby("genero").count


        st.bar_chart(total_por_genero)


    st.subheader("Todas os empréstimos registrados")

    st.dataframe(df, use_container_width=True)

    with st.expander(" Excluir uma registro"):

        id_para_excluir = st.number_input(
            "ID do registro a excluir:",
            min_value=0,
            step=1
        )
       

        if st.button("Excluir"):
           
            excluir_registros(id_para_excluir)
       
            st.success(
                f"Registro com id {id_para_excluir} excluído."
            )
           
            st.rerun()