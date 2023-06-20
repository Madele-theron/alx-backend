import express from 'express'
import redis from 'redis'
import { promisify } from 'util'


const listProducts = [
    { Id: 1, name: 'Suitcase 250', price: 50, stock: 0 },
    { Id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
    { Id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
    { Id: 4, name: 'Suitcase 1050', price: 550, stock: 15 }
]

function getItemById(id) {
    return listProducts.filter((item) => item.itemId === id)[0];
}

// REDIS

const client = redis.createClient()
const getAsync = promisify(client.get).bind(client)

client.once('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (error) => {
    console.log(`Redis client not connected to the server: ${error.message}`);
});

function reserveStockById(itemId, stock) {
    client.set(`item.${itemId}`, stock)
}

async function getCurrentReservedStockById(itemId) {
    return (await getAsync(`item.${itemId}`));
}

// EXPRESS SERVER
const app = express();
const PORT = 1245;

app.listen(PORT, () => {
    console.log(`server is running in port ${PORT}`)
})

// ROUTES

app.get('/list_products', (request, response) => {
    return response.json(listProducts)
})

app.get('/list_products/:itemId', async (request, response) => {
    const itemId = Number(request.params.itemId);
    const item = getItemById(itemId);
  
    if (!item) {
        response.json({ status: 'Product not found' });
      return;
    }
  
    const currentStock = await getCurrentReservedStockById(itemId);
    const stock =
      currentStock === null ? item.initialAvailableQuantity : currentStock;
  
    item.currentQuantity = stock;
    response.json(item);
  });

  app.get('/reserve_product/:itemId', async (request, response) => {
    const itemId = Number(request.params.itemId);
    const item = getItemById(itemId);

  
    if (!item) {
        response.json({ status: 'Product not found' });
      return;
    }
  
    let currentStock = await getCurrentReservedStockById(itemId);
    if (currentStock === null) currentStock = item.initialAvailableQuantity
    
    if (currentStock <= 0) {
        res.json({ status: 'Not enough stock available', itemId})
        return;
    }

    reserveStockById(itemId, Number(currentStock) - 1);

    res.json({ status: 'Reservation confirmed', itemId });
  });
