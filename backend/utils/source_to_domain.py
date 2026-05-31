def source_to_domain(source):
    mapping = {
        "gov":"gov",
        "edu":"edu",
        "nasa":"nasa.gov",
        "nih":"nih.gov",
        "researchgate":"researchgate.net"
    }

    return mapping.get(source)