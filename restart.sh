#!/bin/bash
echo "Остановка демона Odoo"
sudo service odoo-server stop
echo "Запуск демона Odoo"
sudo service odoo-server start
