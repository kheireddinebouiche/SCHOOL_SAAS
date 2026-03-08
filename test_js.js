const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const dom = new JSDOM(`
    <div id="category-tree"></div>
    <div id="empty-state" class="d-none"></div>
`);
const document = dom.window.document;

function buildHierarchy(items) {
    const root = [];
    const map = {};

    items.forEach(item => {
        item.children = [];
        map[item.id] = item;
    });

    items.forEach(item => {
        if (item.parent_id && map[item.parent_id]) {
            map[item.parent_id].children.push(item);
        } else {
            root.push(item);
        }
    });

    return root;
}

function createNodeElement(node) {
    const hasChildren = node.children && node.children.length > 0;
    
    let paymentBadge = '';
    if (node.payment_category && node.payment_category !== '-') {
        paymentBadge = `<span class="node-badge badge-soft-info"><i class="ri-bank-card-line me-1"></i>${node.payment_category}</span>`;
    } else {
        paymentBadge = `<span class="text-muted fs-11 fst-italic">Non associé</span>`;
    }

    const nodeHtml = `
        <div class="tree-node" id="node-${node.id}">
            <div class="tree-content">
                <div class="tree-toggle ${hasChildren ? '' : 'empty'}" onclick="${hasChildren ? `toggleNode(${node.id})` : ''}">
                    ${hasChildren ? '<i class="ri-arrow-right-s-line" id="icon-' + node.id + '"></i>' : '<i class="ri-checkbox-blank-circle-fill" style="font-size: 6px;"></i>'}
                </div>
                <div class="node-icon">
                    <i class="ri-folder-line"></i>
                </div>
                <div class="node-label">
                    ${node.name}
                </div>
                <div class="node-meta">
                    ${paymentBadge}
                    <div class="node-actions">
                        <button class="btn btn-sm btn-ghost-secondary btn-icon" onclick="openEditModal(${node.id})" title="Modifier">
                            <i class="ri-pencil-fill"></i>
                        </button>
                        <button class="btn btn-sm btn-ghost-danger btn-icon" onclick="deleteCategory(${node.id})" title="Supprimer">
                            <i class="ri-delete-bin-fill"></i>
                        </button>
                    </div>
                </div>
            </div>
            ${hasChildren ? `<div class="tree-children" id="children-${node.id}"></div>` : ''}
        </div>
    `;
    return nodeHtml;
}

function renderTreeNodes(nodes, container) {
    nodes.forEach(node => {
        container.insertAdjacentHTML('beforeend', createNodeElement(node));
        if (node.children && node.children.length > 0) {
            const childContainer = container.querySelector(`#children-${node.id}`);
            renderTreeNodes(node.children, childContainer);
        }
    });
}

function renderTree(data) {
    const container = document.getElementById('category-tree');
    const emptyState = document.getElementById('empty-state');
    
    container.innerHTML = '';
    
    if (!data || data.length === 0) {
        container.classList.add('d-none');
        emptyState.classList.remove('d-none');
        return;
    }

    const hierarchy = buildHierarchy(data);
    renderTreeNodes(hierarchy, container);
}

const rawCategories = [
    {id: 1, name: "Parent", parent_id: null, payment_category: "-"},
    {id: 2, name: "Child", parent_id: 1, payment_category: "-"}
];

try {
    renderTree(rawCategories);
    console.log("Success! Tree rendered.");
    console.log(document.getElementById('category-tree').innerHTML);
} catch (e) {
    console.error("ERROR:", e);
}
