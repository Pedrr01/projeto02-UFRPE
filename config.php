<?php

    if(isset($_POST['botaoCadastrar'])){
        $nome = $_POST['nome'];
        $email = $_POST['email'];
        $senha = $_POST['senha'];
        $confSenha = $_POST['confSenha'];
        $faculdade = $_POST['faculdade'];
        $curso = $_POST['curso'];
        $periodo = $_POST['periodo'];
    }

    if($senha != $confSenha){
        die('Senhas não coincidem.');
    }

    $host = 'Localhost';
    $banco = 'campuslink';
    $user = 'root';
    $senha_user = '';

    $con = mysqli_connect($host, $user, $senha_user, $banco);

    if(!$con){
        die('Erro na conexão' . mysqli_connect_error() );
    }

    $sql = "INSERT INTO usuarios(Nome, Email, Senha, Faculdade, Curso, Periodo) VALUES('$nome', '$email', '$senha', '$faculdade', '$curso', '$periodo')";

    $rs = mysqli_query($con, $sql);

    if($rs){
        echo"Cadastro realizado com sucesso.";
    }
?>