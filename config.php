<?php

$Nome = $Email = $Senha = $confSenha = $Faculdade = $Curso = $Periodo = '';
$NomeErro = $EmailErro = $SenhaErro = $confSenhaErro = '';


    if($_SERVER["REQUEST_METHOD"] == "POST"){
        $Nome = $_POST['nome'];
        $Email = $_POST['email'];
        $Senha = $_POST['senha'];
        $confSenha = $_POST['confSenha'];
        $Faculdade = $_POST['faculdade'];
        $Curso = $_POST['curso'];
        $Periodo = $_POST['periodo'];

        if (empty($Nome)) {
            $NomeErro = 'Insira seu nome.';
        }
        if (!filter_var($Email, FILTER_VALIDATE_EMAIL) || !str_ends_with($Email, '@ufrpe.br')){
            $EmailErro = 'Insira um email com domínio @ufrpe.br';
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
    $senha_user = '';

    $con = mysqli_connect($host, $user, $senha_user, $banco);

    if(!$con){
        die('Erro na conexão' . mysqli_connect_error());
    }

    $smt = $con-> prepare ("INSERT INTO usuarios (Nome, Email, Senha, Faculdade, Curso, Periodo) VALUES (?, ?, ?, ?, ?, ?)");
    $smt->bind_param('ssssss' , $Nome, $Email, $Senha, $Faculdade, $Curso, $Periodo);

    if ($smt->execute()) {
        echo"Cadastro realizado com sucesso.";
    }else{ 
        echo"Erro ao realizar o cadastro" . $smt->error; 
    }
    
    $smt->close();
    mysqli_close($con);
}
}