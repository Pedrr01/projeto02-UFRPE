<?php

$Nome = $Email = $senha = $confSenha = $Faculdade = $Curso = $Periodo = '';
$NomeErro = $EmailErro = $SenhaErro = $confSenhaErro = $MensagemErro = '';


    if($_SERVER["REQUEST_METHOD"] == "POST"){
        $Nome = $_POST['nome'];
        $Email = $_POST['email'];
        $Senha = $_POST['senha'];
        $confSenha = $_POST['confsenha'];
        $Faculdade = $_POST['faculdade'];
        $Curso = $_POST['curso'];
        $Periodo = $_POST['periodo'];

        if (empty($Nome)) {
            $NomeErro = 'Insira seu nome.';
        }
        if (empty($Email)) {
            $EmailErro = 'Insira seu email.';
        }
        if (empty($Senha)) {
            $SenhaErro = 'Insira sua senha.';
        }
        if ($Senha != $confSenha) {
            $confSenhaErro = 'As senhas não coincidem.';
        }


if (empty($NomeErro) && empty($EmailErro) && empty($SenhaErro) && empty($confSenhaErro)) {

    $host = 'localhost';
    $banco = 'campuslink';
    $user = 'root';
    $senha_banco = '';

    $con = mysqli_connect($host, $user, $senha_banco, $banco);

    if(!$con){
        die('Erro na conexão' . mysqli_connect_error());
    }

    $sql = "INSERT INTO usuarios(Nome, Email, Senha, Faculdade, Curso, Periodo) VALUES('$Nome', '$Email', '$Senha', '$Faculdade', '$Curso', '$Periodo')";

    $rs = mysqli_query($con, $sql);

    if($rs){
        echo"Cadastro realizado com sucesso.";
    }else{ 
        echo"Erro ao realizar o cadastro";
    }
    mysqli_close($con);
}
    }

