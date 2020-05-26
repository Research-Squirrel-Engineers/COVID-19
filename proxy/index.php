<?php

require 'AltoRouter.php';

$router = new AltoRouter();
$router->setBasePath('/data');

$router->map('GET','/',  function() {
    echo 'test';
} , 'plan2');
$router->map('GET','/[i:id]',  function($id) {
    echo 'id: <b>'.$id.'</b>';
} , 'plan');
$match = $router->match();

if( $match && is_callable( $match['target'] ) ) {
    call_user_func_array( $match['target'], $match['params'] );
} else {
    header( $_SERVER["SERVER_PROTOCOL"] . ' 404 Not Found');
}
