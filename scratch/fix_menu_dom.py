with open('templates/tenant_folder/menu.html', 'r', encoding='utf-8') as f:
    content = f.read()

target1 = """                                                    <div class="submenu-item bg-light bg-opacity-50 rounded-2 mb-1">
                                                        <a href="{% url 't_tresorerie:payment_type_list' %}" class="nav-link {% if request.resolver_match.url_name == 'payment_type_list' %}active{% endif %} d-flex align-items-center py-1 px-2 rounded-2">
                                                            <i class="ri-bank-card-line me-1"></i>
                                                            <span>Types de paiement</span>
                                                        </a>
                                                    </div>
                                                </div>
                                            </div>



                                            <div class="col-12 mt-2">
                                                <a href="#sidebarEcheanciers\""""

replacement1 = """                                                    <div class="submenu-item bg-light bg-opacity-50 rounded-2 mb-1">
                                                        <a href="{% url 't_tresorerie:payment_type_list' %}" class="nav-link {% if request.resolver_match.url_name == 'payment_type_list' %}active{% endif %} d-flex align-items-center py-1 px-2 rounded-2">
                                                            <i class="ri-bank-card-line me-1"></i>
                                                            <span>Types de paiement</span>
                                                        </a>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>



                                            <div class="col-12 mt-2">
                                                <a href="#sidebarEcheanciers\""""

content = content.replace(target1, replacement1)

target2 = """                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                    <!-- Finance -->"""

replacement2 = """                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                    </li>
                    <!-- Finance -->"""

content = content.replace(target2, replacement2)

with open('templates/tenant_folder/menu.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done fixing DOM')
