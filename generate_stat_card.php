<?php
require_once 'lib/php/textpainter.php';

header("Content-type: image/png");

$stats = file_get_contents('data/s.txt');
list($threes, $threes_attempted, $games, $next) = explode(',', $stats);

$x = $_GET['x'];
$y = $_GET['y'];

$x2 = $_GET['x2'];
$y2 = $_GET['y2'];

$x3 = $_GET['x3'];
$y3 = $_GET['y3'];

$f = $_GET['f'];
$f2 = $_GET['f2'];
$f3 = $_GET['f3'];

// Convert strings from stats file to integers.
$threes = intval($threes);
$threes_attempted = intval($threes_attempted);
$games = intval($games);

// Compute pace and round down.
$pace = floatval($threes/$games*82);
$pace = round($pace, 0, PHP_ROUND_HALF_DOWN);

// Compute 3pt% and round to nearest tenth.
$pct = floatval($threes/$threes_attempted*100);
$pct = round($pct, 1, PHP_ROUND_HALF_DOWN);

$img = new textPainter('static/img/currycardbg.png', '', 'static/fonts/font.ttf', 80);

// Grey
$img->setTextColor(160, 160, 160);

$img->setText('THREES', 472, 84, 50);
$img->setText('GAMES', 472, 154, 55);
$img->setText('PACE', 566, 208, 42);
$img->setText('3PT%', 566, 257, 36);

$img->setText('www.scthrees.com', 592, 383, 16);
$img->setText('#curry3count', 634, 359, 16);

// White
$img->setTextColor(255, 255, 255);

$img->setText($threes, 688, 84, 50);
$img->setText($games, 688, 154, 55);
$img->setText($pct, 688, 257, 36);
$img->setText('Stephen Curry', 587, 311, 21.38);
$img->setText('2015-2016   3pt   stats', 587, 335, 16);

// Warriors yellow
$img->setTextColor(251, 220, 5);

$img->setText($pace, 688, 208, 42);

$img->setQuality(100);

$img->show();

?>