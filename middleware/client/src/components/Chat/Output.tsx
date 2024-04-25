import Message from "./Message";

export default function ({ className }: { className?: string }) {
    return (
        <div className={`flex flex-col ${className}`}>
            <Message
                role={"user"}
                message={
                    "Lorem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el texto de relleno estándar de las industrias desde el año 1500, cuando un impresor (N. del T. persona que se dedica a la imprenta) desconocido usó una galería de textos y los mezcló de tal manera que logró hacer un libro de textos especimen. No sólo sobrevivió 500 años, sino que tambien ingresó como texto de relleno en documentos electrónicos, quedando esencialmente igual al original. Fue popularizado en los 60s con la creación de las hojas , las cuales contenian pasajes de Lorem Ipsum, y más recientemente con software de autoedición, como por ejemplo Aldus PageMaker, el cual incluye versiones de Lorem Ipsum."
                }
            />

            <Message
                role={"assistant"}
                message={
                    "Lorem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el texto de relleno estándar de las industrias desde el año 1500, cuando un impresor (N. del T. persona que se dedica a la imprenta) desconocido usó una galería de textos y los mezcló de tal manera que logró hacer un libro de textos especimen. No sólo sobrevivió 500 años, sino que tambien ingresó como texto de relleno en documentos electrónicos, quedando esencialmente igual al original. Fue popularizado en los 60s con la creación de las hojas , las cuales contenian pasajes de Lorem Ipsum, y más recientemente con software de autoedición, como por ejemplo Aldus PageMaker, el cual incluye versiones de Lorem Ipsum."
                }
                lsmResponse={{
                    docs: [{ doc: 1 }, { doc: 2 }],
                    terms: ["term1", "term2"],
                    message: "The example msg",
                    conclusion: "The conclusion",
                }}
            />

            <Message
                role={"user"}
                message={
                    "Lorem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el texto de relleno estándar de las industrias desde el año 1500, cuando un impresor (N. del T. persona que se dedica a la imprenta) desconocido usó una galería de textos y los mezcló de tal manera que logró hacer un libro de textos especimen. No sólo sobrevivió 500 años, sino que tambien ingresó como texto de relleno en documentos electrónicos, quedando esencialmente igual al original. Fue popularizado en los 60s con la creación de las hojas , las cuales contenian pasajes de Lorem Ipsum, y más recientemente con software de autoedición, como por ejemplo Aldus PageMaker, el cual incluye versiones de Lorem Ipsum."
                }
            />
            <Message
                role={"assistant"}
                message={
                    "Lorem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el texto de relleno estándar de las industrias desde el año 1500, cuando un impresor (N. del T. persona que se dedica a la imprenta) desconocido usó una galería de textos y los mezcló de tal manera que logró hacer un libro de textos especimen. No sólo sobrevivió 500 años, sino que tambien ingresó como texto de relleno en documentos electrónicos, quedando esencialmente igual al original. Fue popularizado en los 60s con la creación de las hojas , las cuales contenian pasajes de Lorem Ipsum, y más recientemente con software de autoedición, como por ejemplo Aldus PageMaker, el cual incluye versiones de Lorem Ipsum."
                }
                lsmResponse={{
                    docs: [
                        { doc: 1 },
                        { doc: 2 },
                        {
                            glossary: {
                                title: "example glossary",
                                GlossDiv: {
                                    title: "S",
                                    GlossList: {
                                        GlossEntry: {
                                            ID: "SGML",
                                            SortAs: "SGML",
                                            GlossTerm:
                                                "Standard Generalized Markup Language",
                                            Acronym: "SGML",
                                            Abbrev: "ISO 8879:1986",
                                            GlossDef: {
                                                para: "A meta-markup language, used to create markup languages such as DocBook.",
                                                GlossSeeAlso: ["GML", "XML"],
                                            },
                                            GlossSee: "markup",
                                        },
                                    },
                                },
                            },
                        },
                    ],
                    terms: ["term1", "term2"],
                    message: "The example msg",
                    conclusion: "The conclusion",
                }}
            />
        </div>
    );
}
