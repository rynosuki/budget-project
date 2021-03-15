-- --------------------------------------------------------
-- Värd:                         localhost
-- Serverversion:                8.0.23 - MySQL Community Server - GPL
-- Server-OS:                    Win64
-- HeidiSQL Version:             11.1.0.6116
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumpar data för tabell budgetproject.expenses: ~4 rows (ungefär)
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT IGNORE INTO `expenses` (`id`, `amount`, `contributor`, `source`, `date`, `note`) VALUES
	(1, 320, 'Robin', 'ICA', '2021-05-05', 'Köpte mat'),
	(2, 100, 'Robin', 'ICA', '2021-04-05', 'Mat'),
	(5, 604, 'Robin', 'ICA', '2021-01-05', 'Mat'),
	(6, 4145, 'Robin', 'ICA', '2021-02-05', 'Mat'),
	(7, 6435, 'Robin', 'ICA', '2021-03-05', 'Mat');
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;

-- Dumpar data för tabell budgetproject.income: ~6 rows (ungefär)
/*!40000 ALTER TABLE `income` DISABLE KEYS */;
INSERT IGNORE INTO `income` (`id`, `amount`, `contributor`, `source`, `date`) VALUES
	(1, 150, 'Robin', 'CSN', '2021-03-12'),
	(2, 1500, 'Emelie', 'CSN', '2021-03-15'),
	(3, 300, 'Robin', 'CSN', '2021-01-22'),
	(4, 3150, 'Robin', 'CSN', '2021-04-12'),
	(5, 2100, 'Emelie', 'CSN', '2021-02-12'),
	(6, 600, 'Robin', 'CSN', '2021-05-16');
/*!40000 ALTER TABLE `income` ENABLE KEYS */;

-- Dumpar data för tabell budgetproject.items: ~4 rows (ungefär)
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT IGNORE INTO `items` (`expenseid`, `name`, `price`, `quantity`, `type`) VALUES
	(2, 'Mjölk', 10, 10, 'Mat'),
	(7, 'Mjölk', 10, 5, 'Quornfärs'),
	(7, 'Färs', 49, 2, 'Quornfärs'),
	(7, 'Godis', 152, 1, 'Snacks');
/*!40000 ALTER TABLE `items` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
