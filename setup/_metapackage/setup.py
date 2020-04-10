import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-grap-grap-odoo-incubator",
    description="Meta package for grap-grap-odoo-incubator Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-product_category_usage_group',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
