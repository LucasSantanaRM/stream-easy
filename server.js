const axios = require('axios');
const fs = require('fs');
require('dotenv').config();

const selectedToken = process.env.TOKEN_IXC;
const selectedHost = process.env.URL_IXC;

const options = {
  method: 'GET',
  url: `https://${selectedHost}/webservice/v1/su_oss_chamado`,
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Basic ${Buffer.from(selectedToken).toString("base64")}`,
    ixcsoft: 'listar',
  },
  body: {
    qtype: 'su_oss_chamado.id',
    query: '0',
    oper: '>',
    page: '1',
    rp: '1',
    sortname: 'su_oss_chamado.id',
    sortorder: 'desc',
    grid_param: JSON.stringify([
      {
        TB: 'su_oss_chamado.data_fechamento',
        display: 'Fechamento',
        OP: 'BE',
        P: '2024-07-01 00:00:00',
        P2: '2024-07-31 23:59:59',
        C: 'AND',
        G: '_su_oss_chamado.data_fechamento'
      },
      {
        TB: 'su_oss_chamado.status',
        display: 'Status',
        OP: 'IN',
        P: 'F',
        C: 'AND',
        G: '_su_oss_chamado.status'
      },
      {
        TB: 'su_oss_chamado.id_filial',
        display: 'Filial',
        OP: '=',
        P: '9',
        C: 'AND',
        G: '_su_oss_chamado.id_filial'
      },
      {
        TB: 'su_oss_chamado.data_abertura',
        display: 'Abertura',
        OP: 'BE',
        P: '2024-07-01 00:00:00',
        P2: '2024-07-31 23:59:59',
        C: 'AND',
        G: '_su_oss_chamado.data_abertura'
      },
      {
        TB: 'su_oss_assunto.assunto',
        display: 'Assunto',
        OP: '=',
        P: 'UNI - Instalação Rádio',
        C: 'AND',
        G: '_su_oss_assunto.assunto'
      }
    ]),
    grid_param2: 'false'
  },
  json: true
};

axios(options)
  .then(response => {
    // Salvar dados em DB.json
    fs.writeFile('DB.json', JSON.stringify(response.data, null, 2), (err) => {
      if (err) {
        console.error('Erro ao salvar o arquivo DB.json', err);
      } else {
        console.log('Dados salvos em DB.json');
      }
    });
  })
  .catch(error => {
    console.error('Erro ao buscar dados', error);
  });
